from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views import View
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate
import json

@permission_classes([AllowAny])
class GenerateAnsView(View):
    def get(self, request):
        input_text = request.GET.get('input_text', '')

        # Initialize language model
        llm = CTransformers(
            model='/home/asplggnadmin/Desktop/LQuora/api_project/api/models/Llama-2-7b-chat-finetune.gguf',
            model_type='llama2',
            config={'max_new_tokens': 400,'temperature': 0.01,'context_length': 700}
        )

        # Define prompt template
        template = """{input_text}
        """

        prompt = PromptTemplate(
            input_variables=["input_text"],
            template=template,
            prompt_length=150,
            temperature=0.7,
            max_tokens=100,
            stop_sequence="\n",
            top_p=0.9,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            best_of=3,
            logit_bias={"100": 2, "101": -1},
            use_cache=False,
            return_full=True,
            user_context="The character is in a forest."
        )

        # Generate response from the language model
        response = llm.invoke(prompt.format(input_text=input_text))

        # Debug logging to inspect the raw response
        print("Raw response from language model:", response)

        # Find the first occurrence of '{' and the last occurrence of '}' to cover nested JSON objects
        start_index = response.find('{')
        end_index = response.rfind('}')

        if start_index != -1 and end_index != -1:
            json_str = response[start_index:end_index + 1]

            try:
                # Attempt to parse the JSON string
                extracted_json = json.loads(json_str)

                # Convert JSON to paragraph
                paragraph = ' '.join(f'{key}: {value}.' for key, value in extracted_json.items())
                return JsonResponse({'response': paragraph})
            except json.JSONDecodeError as e:
                # Handle specific errors if extra data is found
                error_message = str(e)
                print("JSON decode error:", error_message)
                if 'Extra data' in error_message:
                    # Extract valid JSON portion before the error
                    error_position = int(error_message.split('char ')[1].split(')')[0])
                    valid_json_str = json_str[:error_position]
                    try:
                        extracted_json = json.loads(valid_json_str)
                        paragraph = ' '.join(f'{key}: {value}.' for key, value in extracted_json.items())
                        return JsonResponse({'response': paragraph})
                    except json.JSONDecodeError as inner_e:
                        print("Inner JSON decode error:", inner_e)
                        return JsonResponse({'error': 'Failed to decode JSON', 'message': str(inner_e)})
                else:
                    return JsonResponse({'error': 'Failed to decode JSON', 'message': str(e)})
        else:
            # If no JSON object is found, return the entire response as a paragraph
            return JsonResponse({'response': response})

@permission_classes([AllowAny])
class dummy(View):
    def get(self, request):
        question = "Why whenever I get in the shower my girlfriend wants to join?"
        answer = "Isn’t it awful? You would swear that there wasn’t enough hot water to go around!"

        return JsonResponse({'question': question, 'answer': answer})
