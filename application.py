import asyncio
import configparser
import time
from typing import Generator

import streamlit as st
from llama_cpp import Llama

from src.service.chat_service import ChatService

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def build_application(config_directory: str) -> ChatService:
    # dependency injection
    config = configparser.ConfigParser()
    config.read(config_directory)

    chat_model_dir = config["CHAT_MODEL"]["model_directory"]
    generation_model = Llama(
        model_path=chat_model_dir,
        n_ctx=4096,
        n_gpu_layers=-1,
        verbose=False,
    )

    return ChatService(generation_model=generation_model)


async def application(config_directory: str) -> None:
    chat_service = build_application(config_directory)

    def stream_data(response: str) -> Generator[str, None, None]:
        for word in response.split(" "):
            yield word + " "
            time.sleep(0.06)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if question := st.chat_input("konus benimle!"):
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            generated_response = chat_service.answer(
                question=question,
                messages=st.session_state.messages,
            )

            st.write_stream(stream_data(generated_response))

        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append(
            {"role": "assistant", "content": generated_response}
        )


if __name__ == "__main__":
    properties_config = "properties/local.ini"
    asyncio.run(application(config_directory=properties_config))
