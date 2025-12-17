// ContentToolbar - Personalization and Translation toggles for chapter pages
import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import styles from './ContentToolbar.module.css';

const API_URL = 'https://physical-ai-humanoid-robotics-textb-one.vercel.app';

interface ContentToolbarProps {
  chapterId: string;
  originalContent: string;
  onContentChange: (content: string, type: 'original' | 'personalized' | 'translated') => void;
}

export default function ContentToolbar({ chapterId, originalContent, onContentChange }: ContentToolbarProps) {
  const { isAuthenticated, accessToken, user } = useAuth();
  const [activeMode, setActiveMode] = useState<'original' | 'personalized' | 'translated'>('original');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [cachedPersonalized, setCachedPersonalized] = useState<string | null>(null);
  const [cachedTranslated, setCachedTranslated] = useState<string | null>(null);

  const handlePersonalize = async () => {
    if (activeMode === 'personalized') {
      // Switch back to original
      setActiveMode('original');
      onContentChange(originalContent, 'original');
      return;
    }

    if (!isAuthenticated) {
      setError('Please login to personalize content');
      return;
    }

    if (!user?.has_profile) {
      setError('Please complete your profile first');
      return;
    }

    // Use cached if available
    if (cachedPersonalized) {
      setActiveMode('personalized');
      onContentChange(cachedPersonalized, 'personalized');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_URL}/api/personalize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          chapter_id: chapterId,
          content: originalContent,
          use_cache: false,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail?.message || 'Failed to personalize');
      }

      const data = await response.json();
      setCachedPersonalized(data.personalized_content);
      setActiveMode('personalized');
      onContentChange(data.personalized_content, 'personalized');
    } catch (err: any) {
      setError(err.message || 'Failed to personalize content');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTranslate = async () => {
    if (activeMode === 'translated') {
      // Switch back to original
      setActiveMode('original');
      onContentChange(originalContent, 'original');
      return;
    }

    // Use cached if available
    if (cachedTranslated) {
      setActiveMode('translated');
      onContentChange(cachedTranslated, 'translated');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
      };

      // Add auth header if logged in (optional for translation)
      if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
      }

      const response = await fetch(`${API_URL}/api/translate`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          chapter_id: chapterId,
          content: originalContent,
          target_language: 'roman_urdu',
          use_cache: false,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail?.message || 'Failed to translate');
      }

      const data = await response.json();
      setCachedTranslated(data.translated_content);
      setActiveMode('translated');
      onContentChange(data.translated_content, 'translated');
    } catch (err: any) {
      setError(err.message || 'Failed to translate content');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.toolbar}>
      <div className={styles.toolbarInner}>
        <span className={styles.label}>Content Mode:</span>

        <div className={styles.buttonGroup}>
          <button
            className={`${styles.btn} ${activeMode === 'original' ? styles.active : ''}`}
            onClick={() => {
              setActiveMode('original');
              onContentChange(originalContent, 'original');
            }}
            disabled={isLoading}
          >
            Original
          </button>

          <button
            className={`${styles.btn} ${activeMode === 'personalized' ? styles.active : ''}`}
            onClick={handlePersonalize}
            disabled={isLoading}
            title={!isAuthenticated ? 'Login required' : !user?.has_profile ? 'Complete profile first' : 'Personalize for your level'}
          >
            {isLoading && activeMode !== 'translated' ? (
              <span className={styles.spinner} />
            ) : (
              <>
                <svg className={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
                Personalize
              </>
            )}
          </button>

          <button
            className={`${styles.btn} ${activeMode === 'translated' ? styles.active : ''}`}
            onClick={handleTranslate}
            disabled={isLoading}
            title="Translate to Roman Urdu"
          >
            {isLoading && activeMode !== 'personalized' ? (
              <span className={styles.spinner} />
            ) : (
              <>
                <svg className={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M5 8l6 6" />
                  <path d="M4 14l6-6 2-3" />
                  <path d="M2 5h12" />
                  <path d="M7 2h1" />
                  <path d="M22 22l-5-10-5 10" />
                  <path d="M14 18h6" />
                </svg>
                Roman Urdu
              </>
            )}
          </button>
        </div>

        {error && <span className={styles.error}>{error}</span>}
      </div>
    </div>
  );
}
