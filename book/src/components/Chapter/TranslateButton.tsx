// T043, T045: TranslateButton Component
import React, { useState } from 'react';
import styles from './Chapter.module.css';

interface TranslateButtonProps {
  chapterId: string;
  originalContent: string;
  onContentChange: (content: string, language: 'en' | 'roman_urdu') => void;
}

const API_URL = 'https://ai-driven-and-spec-driven-hackathon.vercel.app';

export default function TranslateButton({
  chapterId,
  originalContent,
  onContentChange,
}: TranslateButtonProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [currentLanguage, setCurrentLanguage] = useState<'en' | 'roman_urdu'>('en');
  const [error, setError] = useState<string | null>(null);

  const handleTranslate = async () => {
    if (currentLanguage === 'roman_urdu') {
      // Toggle back to English
      onContentChange(originalContent, 'en');
      setCurrentLanguage('en');
      setError(null);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Get auth token if available (translation works for guests too)
      const token = typeof window !== 'undefined' ? localStorage.getItem('auth_token') : null;
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_URL}/api/translate`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          chapter_id: chapterId,
          content: originalContent,
          target_language: 'roman_urdu',
          use_cache: true,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail?.message || 'Failed to translate content');
      }

      const data = await response.json();
      onContentChange(data.translated_content, 'roman_urdu');
      setCurrentLanguage('roman_urdu');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to translate content');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.buttonContainer}>
      <button
        onClick={handleTranslate}
        disabled={isLoading}
        className={`${styles.actionButton} ${styles.translateButton} ${currentLanguage === 'roman_urdu' ? styles.active : ''}`}
        title={currentLanguage === 'roman_urdu' ? 'Switch back to English' : 'Translate to Roman Urdu'}
      >
        {isLoading ? (
          <>
            <span className={styles.spinner}></span>
            Translating...
          </>
        ) : currentLanguage === 'roman_urdu' ? (
          <>
            <svg className={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="m5 8 6 6" />
              <path d="m4 14 6-6 2-3" />
              <path d="M2 5h12" />
              <path d="M7 2h1" />
              <path d="m22 22-5-10-5 10" />
              <path d="M14 18h6" />
            </svg>
            English
          </>
        ) : (
          <>
            <svg className={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="m5 8 6 6" />
              <path d="m4 14 6-6 2-3" />
              <path d="M2 5h12" />
              <path d="M7 2h1" />
              <path d="m22 22-5-10-5 10" />
              <path d="M14 18h6" />
            </svg>
            Roman Urdu
          </>
        )}
      </button>

      {error && (
        <div className={styles.errorToast}>
          {error}
          <button onClick={() => setError(null)} className={styles.closeError}>x</button>
        </div>
      )}
    </div>
  );
}
