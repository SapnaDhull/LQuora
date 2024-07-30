from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers

## Function To get response from LLAma 2 model

def getLLamaresponse(input_text):

    ### LLama2 model
    llm = CTransformers(model='models\llama-2-7b-chat.Q4_K_S.gguf',
                        model_type='llama',
                        config={'max_new_tokens': 256,
                                'temperature': 0.01})

    ## Prompt Template

    template = """
        Write a question {input_text}.
            """

    prompt = PromptTemplate(input_variables=["input_text"],
                            template=template)

    ## Generate the response from the LLama 2 model
    response = llm.invoke(prompt.format(input_text=input_text))
    return response


input_text = input("Enter the question: ")

print("\nGenerating the answer...\n")

## Final response
response = getLLamaresponse(input_text)
print(response)
