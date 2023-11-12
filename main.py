from fastapi import Request, FastAPI, WebSocket
import json
import asyncio
from fastapi.responses import StreamingResponse

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
    answer_output = break_llm_output_string(response=answer)

    for i in range(len(answer_output)):
        json_stream_chunk = {
            "model": "mistral",
            "created_at": "",
            "response": f"{answer_output[i]}",
            "done": False,
        }

        print(json_stream_chunk)

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


async def generate_fake_llm_reesponse():
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

    continue_dev_second_request_prompt = ""

    try:
        # capturing prompt context
        request_data = json.load(await request.body())
        user_prompt_question = (
            request_data["template"].split("[INST]")[-1].split("[/INST]")[0].strip()
        )
        user_chat_chain_context = ("[INST]").join(
            request_data["template"].split("[INST]")[:-1]
        )

        print(user_prompt_question)

        # NOTE: capturing the continuedev second summarizing request prompt
        # if request_data["template"] == continue_dev_second_request_prompt:
        #     return StreamingResponse(
        #         content=generate_fake_llm_reesponse(), media_type="application/json"
        #     )

        # initiating the bot here
        # currently using a fake llm_response
        output = {
            "answer": "As white light passes through our atmosphere, tiny air molecules cause it to scatter. The scattering caused by these tiny air molecules (known as Rayleigh scattering) increases as the wavelength of light decreases. Violet and blue light have the shortest wavelengths and red light has the longest. Therefore, blue light is scattered more than red light and the sky appears blue during the day. When the Sun is low in the sky during sunrise and sunset, the light has to travel further through the Earths atmosphere."
        }

        print(output["answer"])

        return StreamingResponse(
            content=generate_llm_continuedev_stream(output["answer"]),
            media_type="application/json",
        )

    except json.JSONDecodeError:
        return {"error": "Invalid JSON format int the request body"}
    except KeyError as e:
        return {"error": f"Missing key: {e}"}
