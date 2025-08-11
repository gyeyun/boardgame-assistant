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
        originalContents.put(99L, "게임 목표:\n가장 먼저 15 명성 포인트를 모으는 것이 목표입니다.");
        originalContents.put(100L, "테이블에 펼쳐진 카드들 중 한 종류의 과일이 정확히 5개가 되는 순간, 가장 먼저 종을 쳐서 카드를 획득하는 것이 목표입니다.");
        originalContents.put(101L, "상대 팀보다 먼저 우리 팀의 모든 요원을 찾아내는 것이 목표입니다.");
    }

    @Override
    @Transactional
    public TranslationResponse requestTranslation(TranslationRequest request) {
        // 1. 스프링 저장소에서 원본 텍스트를 조회합니다.
        String originalText = originalContents.get(request.getContentId());
        if (originalText == null) {
            throw new IllegalArgumentException("Content not found with id: " + request.getContentId());
        }

        // 2. 파이썬 서버에 '원본 텍스트'를 직접 담아 번역을 요청합니다.
        PythonPostRequest pythonRequest = new PythonPostRequest(originalText, request.getTargetLanguage());
        PythonPostResponse pythonResponse = restTemplate.postForObject(pythonApiBaseUrl + "/request", pythonRequest, PythonPostResponse.class);

        if (pythonResponse == null || pythonResponse.getTranslatedText() == null) {
            throw new RuntimeException("Failed to get translated text from Python service.");
        }
        String translatedText = pythonResponse.getTranslatedText();

        // 3. 번역 결과를 스프링 DB에 저장합니다.
        Translation newTranslation = Translation.builder()
                .contentId(request.getContentId())
                .language(request.getTargetLanguage())
                .translatedText(translatedText)
                .build();
        
        Translation savedTranslation = translationRepository.save(newTranslation);

        // 4. 프론트엔드에 최종 응답을 반환합니다.
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
    private static class PythonPostRequest {
        @JsonProperty("text_to_translate") // 파이썬 모델의 필드명과 일치시킴
        public String textToTranslate;
        @JsonProperty("target_language")
        public String targetLanguage;

        public PythonPostRequest(String textToTranslate, String targetLanguage) {
            this.textToTranslate = textToTranslate;
            this.targetLanguage = targetLanguage;
        }
    }

    private static class PythonPostResponse {
        @JsonProperty("translated_text")
        private String translatedText;
        public String getTranslatedText() { return translatedText; }
        public void setTranslatedText(String translatedText) { this.translatedText = translatedText; }
    }
}
