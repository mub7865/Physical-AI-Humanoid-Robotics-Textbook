// T020: Signup Page
import React, { useState } from 'react';
import Layout from '@theme/Layout';
import SignupForm from '../components/Auth/SignupForm';
import styles from '../components/Auth/Auth.module.css';

type SignupStep = 'signup' | 'success';

interface SignedUpUser {
  id: string;
  email: string;
  name?: string;
}

export default function SignupPage() {
  const [step, setStep] = useState<SignupStep>('signup');
  const [user, setUser] = useState<SignedUpUser | null>(null);

  const handleSignupSuccess = (newUser: SignedUpUser) => {
    setUser(newUser);
    setStep('success');
  };

  const handleSwitchToLogin = () => {
    if (typeof window !== 'undefined') {
      window.location.href = '/Physical-AI-Humanoid-Robotics-Textbook/login';
    }
  };

  const renderContent = () => {
    switch (step) {
      case 'signup':
        return (
          <SignupForm
            onSignupSuccess={handleSignupSuccess}
            onSwitchToLogin={handleSwitchToLogin}
          />
        );

      case 'success':
        return (
          <div className={styles.authContainer}>
            <h2 className={styles.authTitle}>Account Created!</h2>
            <p className={styles.authSubtitle}>
              Your account has been created successfully.
            </p>
            <p style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
              Please sign in to complete your profile setup.
            </p>
            <button
              className={styles.submitButton}
              onClick={() => {
                if (typeof window !== 'undefined') {
                  window.location.href = '/Physical-AI-Humanoid-Robotics-Textbook/login?setup=profile';
                }
              }}
            >
              Continue to Sign In
            </button>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <Layout title="Sign Up" description="Create your account">
      <div className={styles.authPage}>
        {renderContent()}
      </div>
    </Layout>
  );
}
