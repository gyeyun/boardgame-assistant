package com.boardgame.backend_spring.translate.service;

import com.boardgame.backend_spring.translate.dto.*;
import com.boardgame.backend_spring.translate.entity.Translation;
import com.boardgame.backend_spring.translate.repository.TranslationRepository;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class TranslateServiceImpl implements TranslateService {

    private final TranslationRepository translationRepository;
    private final RestTemplate restTemplate;

    // 파이썬 FastAPI 서버 주소
    private final String pythonApiBaseUrl = "http://localhost:8000/api/translate";

    // 원본 콘텐츠를 임시로 저장하는 메모리 내 저장소 (실제로는 Content Repository에서 조회해야 함)
    private static final Map<Long, String> originalContents = new ConcurrentHashMap<>();
    static {
        // 이 부분은 파이썬 서버의 dummy_contents와 동일한 ID를 가져야 합니다.
        originalContents.put(99L, "게임 목표:\n가장 먼저 15 명성 포인트를 모으는 것이 목표입니다.");
        originalContents.put(100L, "테이블에 펼쳐진 카드들 중 한 종류의 과일이 정확히 5개가 되는 순간, 가장 먼저 종을 쳐서 카드를 획득하는 것이 목표입니다.");
        originalContents.put(101L, "상대 팀보다 먼저 우리 팀의 모든 요원을 찾아내는 것이 목표입니다.");
    }

    @Override
    @Transactional
    public TranslationResponse requestTranslation(TranslationRequest request) {
        // 1. 원본 콘텐츠 존재 여부 확인 (스프링 서버 내)
        if (!originalContents.containsKey(request.getContentId())) {
            throw new IllegalArgumentException("Content not found with id: " + request.getContentId());
        }

        // 2. 파이썬 서버에 1차 요청 (번역 요청)
        PythonPostRequest pythonRequest = new PythonPostRequest(request.getContentId(), request.getTargetLanguage());
        PythonPostResponse pythonPostResponse = restTemplate.postForObject(pythonApiBaseUrl + "/request", pythonRequest, PythonPostResponse.class);

        if (pythonPostResponse == null) {
            throw new RuntimeException("Failed to get response from Python service for translation request.");
        }
        
        // 3. 파이썬 서버에 2차 요청 (번역 결과 조회)
        long translatedContentIdFromPython = pythonPostResponse.getTranslatedContentId();
        PythonGetResponse pythonGetResponse = restTemplate.getForObject(pythonApiBaseUrl + "/content/" + translatedContentIdFromPython, PythonGetResponse.class);

        if (pythonGetResponse == null || pythonGetResponse.getText() == null) {
            throw new RuntimeException("Failed to get translated text from Python service.");
        }
        String translatedText = pythonGetResponse.getText();

        // 4. 번역 결과를 스프링 DB에 저장
        Translation newTranslation = Translation.builder()
                .contentId(request.getContentId())
                .language(request.getTargetLanguage())
                .translatedText(translatedText)
                .build();
        
        Translation savedTranslation = translationRepository.save(newTranslation);

        // 5. 프론트엔드에 최종 응답 반환
        return new TranslationResponse(savedTranslation.getTranslationId(), "pending_review");
    }

    @Override
    public TranslateResultResponse getTranslateResult(Long contentId) {
        String originalText = originalContents.get(contentId);
        if (originalText == null) {
             throw new IllegalArgumentException("Content not found with id: " + contentId);
        }

        List<Translation> translations = translationRepository.findByContentId(contentId);
        List<TranslateResultResponse.TranslatedText> translatedTexts = translations.stream()
                .map(t -> new TranslateResultResponse.TranslatedText(t.getLanguage(), t.getTranslatedText()))
                .collect(Collectors.toList());

        return new TranslateResultResponse(contentId, originalText, translatedTexts);
    }

    @Override
    @Transactional
    public TranslationReviewResponse reviewTranslation(TranslationReviewRequest request) {
        String status = "approve".equals(request.getResult()) ? "approved" : "rejected";
        return new TranslationReviewResponse(request.getTranslatedContentId(), status);
    }

    // --- 파이썬 서버와 통신하기 위한 내부 DTO ---

    // POST /request 용
    private static class PythonPostRequest {
        public long contentId;
        public String targetLanguage;
        public PythonPostRequest(long contentId, String targetLanguage) {
            this.contentId = contentId;
            this.targetLanguage = targetLanguage;
        }
    }

    private static class PythonPostResponse {
        private long translatedContentId;
        public long getTranslatedContentId() { return translatedContentId; }
        public void setTranslatedContentId(long translatedContentId) { this.translatedContentId = translatedContentId; }
    }

    // GET /content/{id} 용
    private static class PythonGetResponse {
        private long contentId;
        private String text;
        public long getContentId() { return contentId; }
        public void setContentId(long contentId) { this.contentId = contentId; }
        public String getText() { return text; }
        public void setText(String text) { this.text = text; }
    }
}