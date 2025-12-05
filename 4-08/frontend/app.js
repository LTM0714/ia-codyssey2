const API_BASE_URL = 'http://localhost:8000/api/question';

// 전역 상태
let currentQuestionId = null;
let questions = [];

// 페이지 로드 시 질문 목록 불러오기
document.addEventListener('DOMContentLoaded', () => {
    loadQuestions();
});

// 질문 목록 불러오기
async function loadQuestions() {
    try {
        const response = await fetch(API_BASE_URL);
        if (!response.ok) throw new Error('질문 목록을 불러오는데 실패했습니다.');
        
        questions = await response.json();
        renderQuestionList();
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('question-list').innerHTML = 
            '<p class="error">질문 목록을 불러오는데 실패했습니다.</p>';
    }
}

// 질문 목록 렌더링
function renderQuestionList() {
    const listContainer = document.getElementById('question-list');
    
    if (questions.length === 0) {
        listContainer.innerHTML = `
            <div class="empty-state">
                <p>등록된 질문이 없습니다.</p>
                <button class="btn btn-primary" onclick="showCreateForm()">첫 질문 작성하기</button>
            </div>
        `;
        return;
    }

    listContainer.innerHTML = questions.map(question => {
        const date = new Date(question.create_date).toLocaleString('ko-KR');
        const contentPreview = question.content.length > 100 
            ? question.content.substring(0, 100) + '...' 
            : question.content;
        
        return `
            <div class="question-item" onclick="viewQuestion(${question.id})">
                <div class="question-item-header">
                    <div>
                        <h3>${escapeHtml(question.subject)}</h3>
                        <span class="date">${date}</span>
                    </div>
                </div>
                <div class="content-preview">${escapeHtml(contentPreview)}</div>
                <div class="question-item-actions" onclick="event.stopPropagation()">
                    <button class="btn btn-primary" onclick="editQuestionById(${question.id})">수정</button>
                    <button class="btn btn-danger" onclick="deleteQuestionById(${question.id})">삭제</button>
                </div>
            </div>
        `;
    }).join('');
}

// 질문 상세 보기
async function viewQuestion(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/${id}`);
        if (!response.ok) throw new Error('질문을 불러오는데 실패했습니다.');
        
        const question = await response.json();
        currentQuestionId = question.id;
        
        showQuestionDetail(question);
    } catch (error) {
        console.error('Error:', error);
        alert('질문을 불러오는데 실패했습니다.');
    }
}

// 질문 상세 화면 표시
function showQuestionDetail(question) {
    const detailSection = document.getElementById('question-detail-section');
    const detailContainer = document.getElementById('question-detail');
    const date = new Date(question.create_date).toLocaleString('ko-KR');
    
    detailContainer.innerHTML = `
        <h3>${escapeHtml(question.subject)}</h3>
        <div class="date">작성일: ${date}</div>
        <div class="content">${escapeHtml(question.content)}</div>
    `;
    
    hideAllSections();
    detailSection.classList.remove('hidden');
}

// 질문 작성 폼 표시
function showCreateForm() {
    currentQuestionId = null;
    document.getElementById('question-form').reset();
    document.getElementById('question-id').value = '';
    document.getElementById('form-title').textContent = '새 질문 작성';
    
    hideAllSections();
    document.getElementById('question-form-section').classList.remove('hidden');
}

// 질문 수정 폼 표시
async function editQuestion() {
    if (!currentQuestionId) return;
    await editQuestionById(currentQuestionId);
}

async function editQuestionById(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/${id}`);
        if (!response.ok) throw new Error('질문을 불러오는데 실패했습니다.');
        
        const question = await response.json();
        currentQuestionId = question.id;
        
        document.getElementById('question-id').value = question.id;
        document.getElementById('subject').value = question.subject;
        document.getElementById('content').value = question.content;
        document.getElementById('form-title').textContent = '질문 수정';
        
        hideAllSections();
        document.getElementById('question-form-section').classList.remove('hidden');
    } catch (error) {
        console.error('Error:', error);
        alert('질문을 불러오는데 실패했습니다.');
    }
}

// 폼 제출 처리
async function handleSubmit(event) {
    event.preventDefault();
    
    const id = document.getElementById('question-id').value;
    const subject = document.getElementById('subject').value;
    const content = document.getElementById('content').value;
    
    const questionData = {
        subject: subject,
        content: content
    };
    
    try {
        let response;
        if (id) {
            // 수정
            response = await fetch(`${API_BASE_URL}/${id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(questionData)
            });
        } else {
            // 생성
            response = await fetch(API_BASE_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(questionData)
            });
        }
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || '질문 저장에 실패했습니다.');
        }
        
        await loadQuestions();
        hideForm();
        alert(id ? '질문이 수정되었습니다.' : '질문이 등록되었습니다.');
    } catch (error) {
        console.error('Error:', error);
        alert(error.message || '질문 저장에 실패했습니다.');
    }
}

// 질문 삭제
async function deleteQuestion() {
    if (!currentQuestionId) return;
    
    if (!confirm('정말로 이 질문을 삭제하시겠습니까?')) {
        return;
    }
    
    await deleteQuestionById(currentQuestionId);
}

async function deleteQuestionById(id) {
    if (!confirm('정말로 이 질문을 삭제하시겠습니까?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) throw new Error('질문 삭제에 실패했습니다.');
        
        await loadQuestions();
        hideDetail();
        alert('질문이 삭제되었습니다.');
    } catch (error) {
        console.error('Error:', error);
        alert('질문 삭제에 실패했습니다.');
    }
}

// 폼 숨기기
function hideForm() {
    document.getElementById('question-form-section').classList.add('hidden');
    document.getElementById('question-form').reset();
    currentQuestionId = null;
}

// 상세 화면 숨기기
function hideDetail() {
    document.getElementById('question-detail-section').classList.add('hidden');
    currentQuestionId = null;
}

// 모든 섹션 숨기기
function hideAllSections() {
    document.getElementById('question-form-section').classList.add('hidden');
    document.getElementById('question-detail-section').classList.add('hidden');
}

// HTML 이스케이프 (XSS 방지)
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

