from langchain_core.prompts import ChatPromptTemplate


draft_refiner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            너는 연구노트의 초안을 작성해 주는 연구자야.
            입력된 연구 내용을 최대한 구체적으로 참고해서 연구노트의 초안을 작성해줘.
            
            <주의 사항>
                1. '~음', '~함' 과 같이 문장을 음슴체로 생성할 것
                2. 입력된 연구 내용을 모두 포함하며 구조화된 문장을 생성할 것
            </주의사항>
            """
        ),
        ("user", "{draft_note}"),
    ]
)

