import openai
import pinecone
from dotenv import load_dotenv
import os

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

### TESTING

from flask import Flask, render_template, request, jsonify

### TESTING


# Load variables
load_dotenv()
pinecone_key = os.getenv("PINECONE_KEY")
openai.api_key = os.getenv("OPENAI_KEY")
index_name = "document-embeddings"
environment = "gcp-starter"
model_name = "gpt-3.5-turbo-16k"
# ans_template = """
#     Use the following pieces of context to answer the question at the end.
#     Pay attention to the tone of the question and use it to determine the 
#     technical familiarity of the user with the product, and then adjust your 
#     answer accordingly. If you do not know the answer, advise the user to 
#     seek help via king wencheng support. {context} 
    
#     Question: {question} Answer tailored to the technical familiarity of 
#     the user:
#     """

ans_template = """
    Context: The following API reference information has been retrieved based on the user's question. Pay attention to function names, parameters, and any mentioned errors. Use this information to provide a technically accurate answer.

    Retrieved API Information: {context}
    
    Question: {question}
    
    Tailored Answer (Adjust complexity based on user's technical familiarity):
"""



# Initialize pinecone session
pinecone.init(api_key=pinecone_key, environment=environment)
index = pinecone.Index(index_name)


# Set up langchain pipeline
vector_db = Pinecone.from_existing_index(index_name=index_name, embedding=OpenAIEmbeddings(openai_api_key=openai.api_key))
vector_db_retriever = vector_db.as_retriever()
prompt_for_chain = PromptTemplate(template = ans_template, input_variables = ["context", "question"])
llm = ChatOpenAI(temperature=0, model_name=model_name, openai_api_key=openai.api_key)
assistant = RetrievalQA.from_chain_type(llm = llm,
                                        retriever = vector_db_retriever,
                                        chain_type = "stuff",
                                        chain_type_kwargs = {"prompt": prompt_for_chain})


### TESTING

def extract_keywords(query):
    """
    Extract key terms from the user's query.

    Parameters:
    - query (str): The user's question.

    Returns:
    list: A list of extracted key terms.
    """
    # Tokenize the query and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(query)
    filtered_words = [word for word in words if word not in stop_words]

    # Further processing can be done here, like identifying nouns or technical terms
    # For simplicity, we're returning the filtered words
    return filtered_words

def construct_query(user_query):
    """
    Construct a dynamic query for the vector database based on the user's question.

    Parameters:
    - user_query (str): The user's question.

    Returns:
    str: A dynamically refined query for the vector database.
    """
    keywords = extract_keywords(user_query)
    refined_query = user_query + ' ' + ' '.join(keywords)
    return refined_query

# Function Definitions
def get_assistant_response(user_query):
    """
    Query the chatbot assistant and get a response.

    Parameters:
    - user_query (str): The query to pass to the assistant.

    Returns:
    str: The assistant's response to the query.
    """
    # Refine the user's query using the construct_query function
    refined_query = construct_query(user_query)

    # Use the refined query in the assistant's run method
    return assistant.run(refined_query)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_query = request.get_json().get('query')
        response = get_assistant_response(user_query)
        return jsonify(response=response)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

### TESTING