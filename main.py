from fastapi import Request, FastAPI
import json
import asyncio
from fastapi.responses import StreamingResponse
from sagemakerbot import SagemakerChatbot
import os

# sourcing AWS environment variables
AWS_ENDPOINT_NAME = os.environ["ENDPOINT_NAME_MISTRAL"]
AWS_REGION_NAME = os.environ["REGION_NAME"]

app = FastAPI()


def break_llm_output_string(response: str):
    """
    Function to convert LLM response output string into smaller streamable chunks
    """
    output = []
    i = 0
    while i + 6 < len(response):
        chunk = response[i : i + 6]
        output.append(chunk)
        i += 6

    if i < len(response):
        output.append(response[i:])
    return output


async def generate_llm_continuedev_stream(answer: str):
    """
    Function takes a string as input, converts it into smaller chunks and streams it
    """
    # convert the stream into streamable chunks
    answer_output = break_llm_output_string(answer)

    for i in range(len(answer_output)):
        json_stream_chunk = {
            "model": "mistral",
            "created_at": "",
            "response": f"{answer_output[i]}",
            "done": False,
        }

        yield json.dumps(json_stream_chunk) + "\n"
        await asyncio.sleep(
            0.01
        )  # NOTE: Editable: 0.01 second delay between each streaming chunk

    # sending the final chunk
    json_stream_chunk = {
        "model": "mistral",
        "created_at": "",
        "response": "",
        "done": True,
        "context": [],
        "total_duration": "",
        "load_duration": "",
        "prompt_eval_count": "",
        "prompt_eval_duration": "",
        "eval_count": 0,
        "eval_duration": 0,
    }

    yield json.dumps(json_stream_chunk) + "\n"
    await asyncio.sleep(
        0.01
    )  # NOTE: Editable: 0.01 second delay between each streaming chunk


async def generate_fake_llm_response():
    """
    Function to stream a fake LLM response
    """
    json_stream_chunk = {
        "model": "mistral",
        "created_at": "",
        "response": "",
        "done": True,
        "context": [],
        "total_duration": "",
        "load_duration": "",
        "prompt_eval_count": "",
        "prompt_eval_duration": "",
        "eval_count": 0,
        "eval_duration": 0,
    }

    yield json.dumps(json_stream_chunk) + "\n"
    await asyncio.sleep(
        0.01
    )  # NOTE: Editable: 0.01 second delay between each streaming chunk


@app.post("/api/generate", response_class=StreamingResponse)
async def stream_continuedev_response(request: Request):
    """
    Continuedev streaming endpoint service
    """

    continue_dev_second_request_prompt = '[INST] ""\n\nPlease write a short title summarizing the message quoted above. Use no more than 10 words: [/INST]'

    try:
        # extracting chat prompt context
        request_data = json.loads(await request.body())
        user_prompt_question = (
            request_data["template"].split("[INST]")[-1].split("[/INST]")[0].strip()
        )
        user_chat_context = ("[INST]").join(
            request_data["template"].split("[INST]")[:-1]
        )

        # NOTE: capturing the continuedev second summarizing request prompt
        if request_data["template"] == continue_dev_second_request_prompt:
            return StreamingResponse(
                content=generate_fake_llm_response(), media_type="application/json"
            )

        # Initiating the sagemaker chain
        sagemaker_bot = SagemakerChatbot(
            endpoint_name=AWS_ENDPOINT_NAME, region_name=AWS_REGION_NAME
        )

        output = sagemaker_bot.chat(chat_context=user_chat_context, question=user_prompt_question)

        # Streaming the output string
        return StreamingResponse(
            content=generate_llm_continuedev_stream(output),
            media_type="application/json",
        )

    except json.JSONDecodeError:
        return {"error": "Invalid JSON format in the request body"}
    except KeyError as e:
        return {"error": f"Missing key: {e}"}
