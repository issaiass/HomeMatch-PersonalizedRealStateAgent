from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv,find_dotenv
import logging
import pandas as pd
import numpy as np
import argparse
import asyncio
import glob
import sys
import os

logging.basicConfig()
logger = logging.getLogger(__name__)
#logger.addHandler(logging.StreamHandler(sys.stdout))
load_dotenv(find_dotenv())

class GPTDescriptor:
    def __init__(self, documents_dir, input_format, model='gpt-3.5-turbo', temperature=0.7, max_tokens=300):
        self.documents_dir = documents_dir
        self.input_format  = input_format
        kwargs = dict(model=model, temperature=temperature, max_tokens=max_tokens)
        self.chat_llm = ChatOpenAI(**kwargs)
        self.prompt = self.build_prompt(input_variables=['neighborhood'])

    def list_files(self):
        return glob.glob(f'{self.documents_dir}/*.{self.input_format}')

    def read_documents(self, documents):
        if self.input_format == 'xlsx':
            return pd.concat([pd.read_excel(doc) for doc in documents])
        if self.input_format == 'csv':
            return pd.concat([pd.read_csv(doc, header=0) for doc in documents])        
        if self.input_format == 'parquet':
            return pd.concat([pd.read_parquet(doc) for doc in documents])

    def build_prompt(self, input_variables):
        template = """Describe como es {neighborhood} en Panamá como vecindad para vivir, resume y lista con nombres de sitios\
        los más prominente para fiestas, hospitales cercanos, accesos a autopista, parques, supermercados, centros deportivos y\
        gimnasio, no mas de 200 palabras."""        
        prompt = PromptTemplate(input_variables=input_variables, template=template)
        return prompt

    def build_message(self, neighborhood):
        messages = [
            SystemMessage(content="Eres un vendedor de bienes raices, tu trabajo es encantar con palabras y demostrar las bondades de los sitios\
            no solo como experiencia de vida, sino un lugar para establecerse."),
            HumanMessage(content=self.prompt.format(neighborhood=neighborhood))
        ]
        return messages

    async def invoke_llm(self, neighborhood):
        logging.info(f'Muliprocessing {neighborhood} started')
        messages = self.build_message(neighborhood=neighborhood)
        response = await self.chat_llm.agenerate([messages])
        logging.info(f'{neighborhood} Multiprocessing Finished')
        return response.generations[0][0].text

    def compile_and_save(self, neighborhood_dict, path, output_format='csv'):
        if output_format=='xlsx':
            pd.DataFrame(neighborhood_dict).to_excel(path, index=False, sheet_name='HomeMatch')
        if output_format=='csv':
            pd.DataFrame(neighborhood_dict).to_csv(path, header=True, index=False)
        if output_format=='parquet':
            pd.DataFrame(neighborhood_dict, axis=1).to_parquet(path, index=False)

import time 

async def main(args):
    documents_dir, output_folder = args.documents_dir, args.output_folder
    input_format, output_format, batch_size = args.input_format, args.output_format, args.batch_size
    model, temperature, max_tokens = args.model, args.temperature, args.max_tokens
    gd = GPTDescriptor(documents_dir=documents_dir, input_format=input_format, model=model, temperature=temperature, max_tokens=max_tokens)
    documents_list = gd.list_files()
    df = gd.read_documents(documents_list)
    neighborhoods = df.neighborhood.unique().tolist()
    results = list()
    for start in range(0, len(neighborhoods), batch_size):
        end = start + batch_size
        neighborhoods_mini_batch = neighborhoods[start:end] 
        tasks = [gd.invoke_llm(neighborhood) for neighborhood in neighborhoods_mini_batch]
        values = await asyncio.gather(*tasks)
        results.extend(values)
    neighborhood_dict = dict(neibhorhood=neighborhoods, neighborhood_description=results)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    path = os.path.join(output_folder, f'neighborhood_descriptions.{output_format}')
    gd.compile_and_save(neighborhood_dict=neighborhood_dict, path=path, output_format=output_format)


if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description='builds a dataframe of the webpages selected')
    parser.add_argument('-d', '--documents-dir', type=str, default='documents')
    parser.add_argument('-o', '--output-folder', type=str, default='description')
    parser.add_argument('-if', '--input-format', type=str, default='csv')
    parser.add_argument('-of', '--output-format', type=str, default='csv')    
    parser.add_argument('-b', '--batch-size', type=int, default=5)
    parser.add_argument('-m', '--model', type=str, default='gpt-3.5-turbo')
    parser.add_argument('-t', '--temperature', type=float, default=0.7)
    parser.add_argument('-k', '--max-tokens', type=int, default=200) 

    args = parser.parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))
