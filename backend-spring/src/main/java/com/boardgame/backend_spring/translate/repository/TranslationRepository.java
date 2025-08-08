package com.boardgame.backend_spring.translate.repository;

import com.boardgame.backend_spring.translate.entity.Translation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TranslationRepository extends JpaRepository<Translation, Long> {

    List<Translation> findByContentId(Long contentId);
}
