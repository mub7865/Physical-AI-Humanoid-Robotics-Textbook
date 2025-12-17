// T035, T038: PersonalizeButton Component
import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import styles from './Chapter.module.css';

interface PersonalizeButtonProps {
  chapterId: string;
  originalContent: string;
  onContentChange: (content: string, isPersonalized: boolean) => void;
}

const API_URL = 'https://ai-driven-and-spec-driven-hackathon.vercel.app';

export default function PersonalizeButton({
  chapterId,
  originalContent,
  onContentChange,
}: PersonalizeButtonProps) {
  const { isAuthenticated, accessToken, user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Only show for authenticated users with profiles
  if (!isAuthenticated || !user?.has_profile) {
    return null;
  }

  const handlePersonalize = async () => {
    if (isPersonalized) {
      // T038: Revert to original
      onContentChange(originalContent, false);
      setIsPersonalized(false);
      setError(null);
      return;
    }

    setIsLoading(true);
    setError(null);

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
          use_cache: true,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail?.message || 'Failed to personalize content');
      }

      const data = await response.json();
      onContentChange(data.personalized_content, true);
      setIsPersonalized(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to personalize content');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.buttonContainer}>
      <button
        onClick={handlePersonalize}
        disabled={isLoading}
        className={`${styles.actionButton} ${isPersonalized ? styles.active : ''}`}
        title={isPersonalized ? 'Revert to original content' : 'Personalize content for your experience level'}
      >
        {isLoading ? (
          <>
            <span className={styles.spinner}></span>
            Personalizing...
          </>
        ) : isPersonalized ? (
          <>
            <svg className={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
              <path d="M3 3v5h5" />
            </svg>
            Revert to Original
          </>
        ) : (
          <>
            <svg className={styles.icon} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
            Personalize for Me
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
