// T019: BackgroundQuestionnaire Component
import React, { useState } from 'react';
import styles from './Auth.module.css';

interface BackgroundQuestionnaireProps {
  onComplete: () => void;
  accessToken: string;
}

type SoftwareExp = 'beginner' | 'intermediate' | 'expert';
type HardwareExp = 'none' | 'arduino_rpi' | 'jetson_industrial';
type RoboticsBg = 'student' | 'hobbyist' | 'professional';

// Live backend URL
const API_URL = 'https://physical-ai-humanoid-robotics-textb-one.vercel.app';

const SOFTWARE_OPTIONS = [
  { value: 'beginner', label: 'Beginner', description: 'Just starting to learn programming' },
  { value: 'intermediate', label: 'Intermediate', description: 'Comfortable with some projects' },
  { value: 'expert', label: 'Expert', description: 'Professional developer experience' },
];

const HARDWARE_OPTIONS = [
  { value: 'none', label: 'None', description: 'Software only background' },
  { value: 'arduino_rpi', label: 'Arduino / Raspberry Pi', description: 'Hobby-level electronics' },
  { value: 'jetson_industrial', label: 'Jetson / Industrial', description: 'Advanced embedded systems' },
];

const ROBOTICS_OPTIONS = [
  { value: 'student', label: 'Student', description: 'Learning robotics in school/courses' },
  { value: 'hobbyist', label: 'Hobbyist', description: 'Personal robotics projects' },
  { value: 'professional', label: 'Professional', description: 'Work experience in robotics' },
];

const LANGUAGE_OPTIONS = ['Python', 'C++', 'ROS', 'JavaScript', 'MATLAB', 'Other'];

export default function BackgroundQuestionnaire({ onComplete, accessToken }: BackgroundQuestionnaireProps) {
  const [step, setStep] = useState(1);
  const [softwareExp, setSoftwareExp] = useState<SoftwareExp>('intermediate');
  const [hardwareExp, setHardwareExp] = useState<HardwareExp>('none');
  const [roboticsBg, setRoboticsBg] = useState<RoboticsBg>('student');
  const [languages, setLanguages] = useState<string[]>(['Python']);
  const [learningGoals, setLearningGoals] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const totalSteps = 4;

  const handleLanguageToggle = (lang: string) => {
    if (languages.includes(lang)) {
      setLanguages(languages.filter((l) => l !== lang));
    } else {
      setLanguages([...languages, lang]);
    }
  };

  const handleSubmit = async () => {
    setError('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/profile`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          software_exp: softwareExp,
          hardware_exp: hardwareExp,
          robotics_bg: roboticsBg,
          languages: languages.map((l) => l.toLowerCase()),
          learning_goals: learningGoals || undefined,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        setError(data.detail?.message || 'Failed to save profile. Please try again.');
        return;
      }

      // Profile saved successfully
      onComplete();
    } catch (err) {
      setError('Network error. Please check your connection and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div className={styles.questionStep}>
            <h3 className={styles.questionTitle}>What is your software development experience?</h3>
            <div className={styles.optionsGrid}>
              {SOFTWARE_OPTIONS.map((opt) => (
                <button
                  key={opt.value}
                  type="button"
                  className={`${styles.optionButton} ${softwareExp === opt.value ? styles.optionSelected : ''}`}
                  onClick={() => setSoftwareExp(opt.value as SoftwareExp)}
                >
                  <span className={styles.optionLabel}>{opt.label}</span>
                  <span className={styles.optionDesc}>{opt.description}</span>
                </button>
              ))}
            </div>
          </div>
        );

      case 2:
        return (
          <div className={styles.questionStep}>
            <h3 className={styles.questionTitle}>What is your hardware/electronics experience?</h3>
            <div className={styles.optionsGrid}>
              {HARDWARE_OPTIONS.map((opt) => (
                <button
                  key={opt.value}
                  type="button"
                  className={`${styles.optionButton} ${hardwareExp === opt.value ? styles.optionSelected : ''}`}
                  onClick={() => setHardwareExp(opt.value as HardwareExp)}
                >
                  <span className={styles.optionLabel}>{opt.label}</span>
                  <span className={styles.optionDesc}>{opt.description}</span>
                </button>
              ))}
            </div>
          </div>
        );

      case 3:
        return (
          <div className={styles.questionStep}>
            <h3 className={styles.questionTitle}>What is your robotics background?</h3>
            <div className={styles.optionsGrid}>
              {ROBOTICS_OPTIONS.map((opt) => (
                <button
                  key={opt.value}
                  type="button"
                  className={`${styles.optionButton} ${roboticsBg === opt.value ? styles.optionSelected : ''}`}
                  onClick={() => setRoboticsBg(opt.value as RoboticsBg)}
                >
                  <span className={styles.optionLabel}>{opt.label}</span>
                  <span className={styles.optionDesc}>{opt.description}</span>
                </button>
              ))}
            </div>
          </div>
        );

      case 4:
        return (
          <div className={styles.questionStep}>
            <h3 className={styles.questionTitle}>Which programming languages do you know?</h3>
            <div className={styles.languageGrid}>
              {LANGUAGE_OPTIONS.map((lang) => (
                <button
                  key={lang}
                  type="button"
                  className={`${styles.languageButton} ${languages.includes(lang) ? styles.languageSelected : ''}`}
                  onClick={() => handleLanguageToggle(lang)}
                >
                  {lang}
                </button>
              ))}
            </div>

            <div className={styles.formGroup} style={{ marginTop: '1.5rem' }}>
              <label htmlFor="learningGoals" className={styles.label}>
                What are your learning goals? (optional)
              </label>
              <textarea
                id="learningGoals"
                value={learningGoals}
                onChange={(e) => setLearningGoals(e.target.value)}
                className={styles.textarea}
                placeholder="E.g., Build a humanoid robot, Learn ROS2, Understand AI for robotics..."
                rows={3}
                maxLength={1000}
              />
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className={styles.authContainer}>
      <h2 className={styles.authTitle}>Tell us about yourself</h2>
      <p className={styles.authSubtitle}>
        This helps us personalize content for your experience level
      </p>

      <div className={styles.progressBar}>
        <div
          className={styles.progressFill}
          style={{ width: `${(step / totalSteps) * 100}%` }}
        />
      </div>
      <p className={styles.stepIndicator}>
        Step {step} of {totalSteps}
      </p>

      {renderStep()}

      {error && <div className={styles.error}>{error}</div>}

      <div className={styles.navButtons}>
        {step > 1 && (
          <button
            type="button"
            className={styles.secondaryButton}
            onClick={() => setStep(step - 1)}
            disabled={isLoading}
          >
            Back
          </button>
        )}

        {step < totalSteps ? (
          <button
            type="button"
            className={styles.submitButton}
            onClick={() => setStep(step + 1)}
          >
            Next
          </button>
        ) : (
          <button
            type="button"
            className={styles.submitButton}
            onClick={handleSubmit}
            disabled={isLoading}
          >
            {isLoading ? 'Saving...' : 'Complete Setup'}
          </button>
        )}
      </div>
    </div>
  );
}
