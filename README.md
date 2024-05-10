# HomeMatch - Personalized Real Estate Agent

## 1 - Project Overview
-    ### 1.1 - Project Introduction
     Imagine you're a talented developer at "Future Homes Realty", a forward-thinking real estate company. In an industry where personalization is key to customer satisfaction, your company wants to revolutionize how clients interact with real estate listings. The goal is to create a personalized experience for each buyer, making the property search process more engaging and tailored to individual preferences.

## 2 - The Challenge
Our task is to develop an innovative application named "HomeMatch". This application leverages large language models (LLMs) and vector databases to transform standard real estate listings into personalized narratives that resonate with potential buyers' unique preferences and needs.

-    ### 2.1 - Core Components of "HomeMatch"
     Understanding Buyer Preferences:
     - Buyers will input their requirements and preferences, such as location, property type, budget, amenities, and lifestyle choices.
     - The application uses LLMs to interpret these inputs in natural language, understanding nuanced requests beyond basic filters.

-    ### 2.2 Integrating with a Vector Database:
     - We will connect "HomeMatch" with a vector database, where all available property listings are stored.
     - Utilize vector embeddings to match properties with buyer preferences, focusing on aspects like neighborhood vibes, architectural styles, and proximity to specific amenities.

-    ### 2.3 - Personalized Listing Description Generation:
     - For each matched listing, use an LLM we have rewritten a description in a way that highlights aspects most relevant to the buyer’s preferences.
     - Ensured  personalization emphasizes characteristics appealing to the buyer without altering factual information about the property.

-    ### 2.4 - Listing Presentation:
     - Finally, the last output shows the personalized listing(s) as a text description of the listing.

## 3- Detailed Home Match Application

-    #### Step 3.1: Setting Up the Python Application
     We initialized a Python Project creating a virtual environment, this environment has the main LangChain library, suitable for LLM development with OpenAI but we can change it, also developed a vector database using ChromaDB.

-    #### Step 3.2: Generating Real Estate Listings
     We generated listings using a combination of LLM and web scrapping of several observations, nearly +300 that looks like:
     - links: https:...
     - description: "Este es un apartamento"
     - apartment_description: "apartamento de dos recamaras...
     - sqm: 70
     - room: 2
     - bathroom: 2
     - parking: 1
     - neighborhood: "Coco del Mar"
     - price: 350000
     - neighborhood_description: "Aprovecha estar en el mejor ... "


-    #### Step 3.3: Storing Listings in a Vector Database
     - Vector Database Setup: configured ChromaDB vector database to store real estate listings.

     - Generating and Storing Embeddings: Convertes the LLM-generated listings into suitable embeddings that capture the semantic content of each listing, and store these embeddings in the vector database.

-    #### Step 3.4: Building the User Preference Interface
     - We collected (as raw and fixed input to the LLM) information such as the number of bedrooms, bathrooms, location, and other specific requirements from a set of questions or telling the buyer to enter their preferences in natural language. 

     - Buyer Preference Parsing: Implemented logic to interpret and structure these preferences for querying the vector database.

-    #### Step 3.5: Searching Based on Preferences
     - Semantic Search Implementation: Used the structured buyer preferences to perform a semantic search on the vector database, retrieving listings that most closely match the user's requirements.
     - Listing Retrieval Logic: Fine-tuned the retrieval algorithm to ensure that the most relevant listings are selected based on the semantic closeness to the buyer’s preferences.

-    #### Step 3.6: Personalizing Listing Descriptions
     - LLM Augmentation: For each retrieved listing, we used the LLM to augment the description, tailoring it to resonate with the buyer’s specific preferences. This involves subtly emphasizing aspects of the property that align with what the buyer is looking for.
     - Maintaining Factual Integrity: Ensured that the augmentation process enhances the appeal of the listing without altering factual information.

-    #### Step 3.7: Deliverables and Testing
     - Finally, we tested our "HomeMatch" application and make sure it will be run. Enter different "buyer preferences" and ensure it works, we used the jupyter notebook Jupyter Notebook approach to compile the application code.

     - Example Outputs: Include an example output showcasing how user preferences are processed and how the application generates personalized listing descriptions.

## 4 - Conclusion 
- We demonstrated that we can improve query of the chatbot adding more information to it and make a chain of the response embeddings to get a final though of what will be the best place to buy
- We also included images in the search, but one better way is the use of CLIP model to make a multimodal search for "HomeMatch".  Due to CloudFlare working on the site "CompreOAlquile" the requested images here were only links.

<details open>
<summary> <b>5 - Results<b></summary>

Look at the end of the notebook for the chain of questions and answer improved.

<p align="center"> </p>
</details>

<details open>
<summary> <b>Issues<b></summary>

- no issues found yet.

</details>

<details open>
<summary> <b>Future Work<b></summary>

- None

</details>

<details open>
<summary> <b>Contributing<b></summary>

Your contributions are always welcome! Please feel free to fork and modify the content but remember to finally do a pull request.

</details>

<details open>
<summary> :iphone: <b>Having Problems?<b></summary>

<p align = "center">

[<img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" />](https://www.linkedin.com/in/riawa)
[<img src="https://img.shields.io/badge/telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/>](https://t.me/issaiass)
[<img src="https://img.shields.io/badge/instagram-%23E4405F.svg?&style=for-the-badge&logo=instagram&logoColor=white">](https://www.instagram.com/daqsyspty/)
[<img src="https://img.shields.io/badge/twitter-%231DA1F2.svg?&style=for-the-badge&logo=twitter&logoColor=white" />](https://twitter.com/daqsyspty) 
[<img src ="https://img.shields.io/badge/facebook-%233b5998.svg?&style=for-the-badge&logo=facebook&logoColor=white%22">](https://www.facebook.com/daqsyspty)
[<img src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" />](https://www.linkedin.com/in/riawe)
[<img src="https://img.shields.io/badge/tiktok-%23000000.svg?&style=for-the-badge&logo=tiktok&logoColor=white" />](https://www.linkedin.com/in/riawe)
[<img src="https://img.shields.io/badge/whatsapp-%23075e54.svg?&style=for-the-badge&logo=whatsapp&logoColor=white" />](https://wa.me/50766168542?text=Hello%20Rangel)
[<img src="https://img.shields.io/badge/hotmail-%23ffbb00.svg?&style=for-the-badge&logo=hotmail&logoColor=white" />](mailto:issaiass@hotmail.com)
[<img src="https://img.shields.io/badge/gmail-%23D14836.svg?&style=for-the-badge&logo=gmail&logoColor=white" />](mailto:riawalles@gmail.com)

</p>


</details>

<details open>
<summary> <b>License<b></summary>
<p align = "center">
<img src= "https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg" />
</p>
</details>