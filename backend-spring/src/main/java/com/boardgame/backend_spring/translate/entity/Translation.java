package com.boardgame.backend_spring.translate.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(name = "translation")
@Getter @Setter
@NoArgsConstructor @AllArgsConstructor @Builder
public class Translation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "translation_id")
    private Long translationId;

    // content_id를 단순히 Long 타입으로 선언. content 엔티티 생기면 연동 필요.
    @Column(name = "content_id", nullable = false)
    private Long contentId; // FK이지만, JPA 관계 매핑은 하지 않음

    @Column(name = "language", length = 100)
    private String language;

    @Column(name = "translated_text", columnDefinition = "TEXT")
    private String translatedText;
}