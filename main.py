from langchain_openai import ChatOpenAI

chat_llm = ChatOpenAI(
    base_url="http://localhost:8080/v1", api_key="none", streaming=True
)

prompt = "안녕하세요, 오늘 날씨에 어울리는 음악 추천해줘."


def main():
    for chunk in chat_llm.stream(prompt):
        print(chunk.content, end="", flush=True)
    print()  # 줄바꿈


if __name__ == "__main__":
    main()
