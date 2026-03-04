from operator import itemgetter

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import trim_messages
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI


def debug_print(x):
    print("----- [모델로 전달되는 최종 입력] -----")
    print(x)  # 또는 x.to_string()
    print("------------------------------------")
    return x


# llm = ChatOpenAI(base_url="http://localhost:8080/v1", api_key="none", streaming=True)

# Ollama Cloud 모델 사용
llm = ChatOpenAI(
    base_url="https://ollama.com/v1",
    model="gpt-oss:20b-cloud",
    api_key="your key",
)

# 대화 기록을 담을 수 있도록 프롬프트를 업데이트합니다.
prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)


# 세션 저장소 (실제 서비스에선 DB 연결 가능)
store = {}


def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


chat_chain = (
    prompt
    | llm
    # RunnableLambda(debug_print) |
    | StrOutputParser()
)

with_history_chain = RunnableWithMessageHistory(
    chat_chain,
    get_session_history,
    input_messages_key="question",  # 사용자의 질문 변수명
    history_messages_key="chat_history",  # 프롬프트 내 기록 변수명
)

# 6. 실행 (세션 ID 지정)
config = {"configurable": {"session_id": "user_456"}}

print("첫 번째 질문:")
for chunk in with_history_chain.stream(
    {"question": "안녕! 내 이름은 빵원이야. 내 나이는 33살이야. 1+1이 뭐야?"},
    config=config,
):
    print(chunk, end="", flush=True)
print("-----")  # 줄바꿈

print("두 번째 질문:")
for chunk in with_history_chain.stream(
    {"question": "내 이름이 무엇이지?"}, config=config
):
    print(chunk, end="", flush=True)
print("-----")  # 줄바꿈


trimmer = trim_messages(
    max_tokens=2,  # 윈도우 크기 (여기서는 메시지 2개)
    strategy="last",  # 마지막 메시지부터 유지
    token_counter=len,  # 개수 기준 (토큰 기준이면 llm.get_num_tokens 사용)
    include_system=True,  # 시스템 메시지는 삭제되지 않도록 보호
    start_on="human",  # 대화의 시작은 항상 사용자로 고정
)

trimmer_chain = (
    RunnablePassthrough.assign(chat_history=itemgetter("chat_history") | trimmer)
    | prompt
    # | RunnableLambda(debug_print)
    | llm
    | StrOutputParser()
)

with_trimmer_history_chain = RunnableWithMessageHistory(
    trimmer_chain,
    get_session_history,
    input_messages_key="question",  # 사용자의 질문 변수명
    history_messages_key="chat_history",  # 프롬프트 내 기록 변수명
)

print("세 번째 질문 (트림 후):")
for chunk in with_trimmer_history_chain.stream(
    {"question": "내 이름이 무엇이지?"}, config=config
):  # 트림된 상태에서 질문 실행
    print(chunk, end="", flush=True)
print("-----")  # 줄바꿈

print("네 번째 질문 (트림 후):")
for chunk in with_trimmer_history_chain.stream(
    {"question": "내 나이가 몇일까?"}, config=config
):  # 트림된 상태에서 질문 실행
    print(chunk, end="", flush=True)
print("-----")  # 줄바꿈
