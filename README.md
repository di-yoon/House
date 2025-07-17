# 서울시 청년 주거지원 정책 챗봇

서울시 청년을 위한 다양한 주거복지 정책을 대화형으로 안내하는 인공지능 챗봇입니다.  
복잡한 정책 문서를 벡터 DB로 요약하고, GPT-4 기반 언어 모델이 질문에 맞는 정확한 정책 정보를 제공합니다.  
<br>

## 주요 기능

-  **자연어 기반 질의 응답**  
  월세, 전세, 임대주택, 주거급여 등 청년 주거 관련 질문을 자유롭게 입력하면 챗봇이 답변합니다.

- **공식 문서 기반 응답**  
  서울시 및 관련 기관의 정책 문서를 벡터화해 실질적인 근거 기반 답변을 생성합니다.

- **대화 맥락 기억**  
  `ConversationBufferMemory`를 활용하여 이전 질문을 기억하고 연속적인 문맥을 유지합니다.

-  **Few-shot 학습 예시 내장**  
  질문/답변 예시를 LLM 프롬프트에 삽입해 더 자연스럽고 정책 맞춤형 답변을 생성합니다.

- **Streamlit UI 제공**  
  로컬 환경에서 바로 웹 브라우저로 챗봇을 사용할 수 있는 간편한 인터페이스를 제공합니다.
<br>

##  작동 방식

1. **문서 벡터화**  
   `create_summerized_vector_store.ipynb`를 통해 정책 문서를 `text-embedding-3-large`로 임베딩하고 `Chroma` 벡터 DB로 저장합니다.

2. **앱 초기화**  
   `main.py`가 벡터 스토어를 불러오고, GPT-4 기반 체인과 검색기를 생성합니다.

3. **질문 처리 흐름**  
   사용자가 `app.py`를 통해 질문 → 벡터 검색 → 문맥 포함 GPT 응답 → 실시간 스트리밍 출력 → 대화 저장
<br>


##  설치 방법

### 1. 가상환경 생성 및 패키지 설치

```bash
bash
conda create -n housing-chatbot python=3.10
conda activate housing-chatbot
pip install -r requirements.txt
```
### 2. .env 파일 설정
.env 파일을 프로젝트 루트에 생성하고 다음 형식으로 작성하세요:
```bash
py
OPENAI_API_KEY=sk-...
SERP_API_KEY=...
GOV_API_KEY=...
PINECONE_API_KEY=...
LANGCHAIN_API_KEY=...
⚠️ .env 파일은 절대 GitHub에 커밋하지 마세요!
```
<br>


## 실행 방법

1. 정책 문서 임베딩
```bash
bash
streamlit run create_summerized_vector_store.ipynb
```
2. 챗봇 실행
```bash
bash
streamlit run app.py
```
<br>

## 프로젝트 구성

| 파일명 | 설명 |
|:--------|:------|
| `app.py` | Streamlit 기반 챗봇 실행 UI 및 세션 관리 |
| `main.py` | 벡터 스토어 로드, LangChain 체인 및 GPT 응답 생성 |
| `myexample.py` | Few-shot 예시 질문/답변 데이터 |
| `create_summerized_vector_store.ipynb` | 정책 문서 임베딩 및 저장 |
| `doc.ipynb` | 정책 데이터 정제/실험용 노트북 |
| `.env` | API 키 환경변수 (비공개) |
| `requirements.txt` | 전체 실행 패키지 목록 |

<br>

## 예시 질문
```bash
Q: 서울에 사는 청년인데 전세자금 대출 이자 지원되나요?  
A: 네, 서울시에서는 '청년 전세자금대출 이자지원 사업'을 통해...  
<br>
Q: 월세 부담이 너무 커요. 청년 월세지원 있나요?  
A: 서울시는 만 19~39세 청년을 대상으로 월 20만원, 최대 10개월간 월세 지원 정책을 운영합니다.
```

## 기여 방법
PR 환영합니다! 주석 개선, 정책 데이터 추가, UI 향상 등 어떤 기여든 좋습니다.

이슈 등록 후 논의해주시면 더 좋아요.

.env나 민감한 데이터는 꼭 .gitignore 처리해주세요.
