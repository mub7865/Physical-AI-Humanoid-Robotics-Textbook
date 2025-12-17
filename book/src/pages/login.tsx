// T028: Login Page
import React, { useState, useEffect } from 'react';
import Layout from '@theme/Layout';
import LoginForm from '../components/Auth/LoginForm';
import BackgroundQuestionnaire from '../components/Auth/BackgroundQuestionnaire';
import styles from '../components/Auth/Auth.module.css';

type LoginStep = 'login' | 'questionnaire' | 'complete';

const BASE_URL = '/Physical-AI-Humanoid-Robotics-Textbook';

export default function LoginPage() {
  const [step, setStep] = useState<LoginStep>('login');
  const [accessToken, setAccessToken] = useState<string>('');
  const [needsProfile, setNeedsProfile] = useState(false);

  useEffect(() => {
    // Check if we came from signup and need to complete profile
    if (typeof window !== 'undefined') {
      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.get('setup') === 'profile') {
        setNeedsProfile(true);
      }
    }
  }, []);

  const handleLoginSuccess = (data: { accessToken: string; user: any }) => {
    setAccessToken(data.accessToken);

    // Store token in localStorage for auth context
    if (typeof window !== 'undefined') {
      localStorage.setItem('auth_token', data.accessToken);
      localStorage.setItem('user', JSON.stringify(data.user));
    }

    // Check if user needs to complete profile
    if (data.user.profile_required || needsProfile) {
      setStep('questionnaire');
    } else {
      // Redirect to home
      if (typeof window !== 'undefined') {
        window.location.href = BASE_URL + '/';
      }
    }
  };

  const handleQuestionnaireComplete = () => {
    setStep('complete');

    // Redirect to home after a short delay
    setTimeout(() => {
      if (typeof window !== 'undefined') {
        window.location.href = BASE_URL + '/';
      }
    }, 1500);
  };

  const handleSwitchToSignup = () => {
    if (typeof window !== 'undefined') {
      window.location.href = BASE_URL + '/signup';
    }
  };

  const renderContent = () => {
    switch (step) {
      case 'login':
        return (
          <LoginForm
            onLoginSuccess={handleLoginSuccess}
            onSwitchToSignup={handleSwitchToSignup}
          />
        );

      case 'questionnaire':
        return (
          <BackgroundQuestionnaire
            accessToken={accessToken}
            onComplete={handleQuestionnaireComplete}
          />
        );

      case 'complete':
        return (
          <div className={styles.authContainer}>
            <h2 className={styles.authTitle}>Welcome!</h2>
            <p className={styles.authSubtitle}>
              Redirecting to the book...
            </p>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <Layout title="Sign In" description="Sign in to your account">
      <div className={styles.authPage}>
        {renderContent()}
      </div>
    </Layout>
  );
}
