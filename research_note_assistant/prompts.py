from langchain_core.prompts import ChatPromptTemplate


draft_refiner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "너는 연구노트의 초안을 작성해 주는 연구자야.\n 입력된 연구 내용을 최대한 구체적으로 참고해서 연구노트의 초안을 작성해줘.",
        ),
        ("user", "{draft_note}"),
    ]
)

