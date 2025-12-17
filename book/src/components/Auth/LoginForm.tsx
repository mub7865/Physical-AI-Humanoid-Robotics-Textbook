// T026: LoginForm Component
import React, { useState } from 'react';
import styles from './Auth.module.css';

interface LoginFormProps {
  onLoginSuccess: (data: { accessToken: string; user: any }) => void;
  onSwitchToSignup: () => void;
}

// Live backend URL
const API_URL = 'https://physical-ai-humanoid-robotics-textb-one.vercel.app';

export default function LoginForm({ onLoginSuccess, onSwitchToSignup }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Include cookies
        body: JSON.stringify({
          email,
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        if (data.detail?.error === 'INVALID_CREDENTIALS') {
          setError('Invalid email or password. Please try again.');
        } else if (data.detail?.error === 'TOO_MANY_ATTEMPTS') {
          setError('Too many login attempts. Please wait a moment and try again.');
        } else {
          setError(data.detail?.message || 'Login failed. Please try again.');
        }
        return;
      }

      // Login successful
      onLoginSuccess({
        accessToken: data.access_token,
        user: data.user,
      });
    } catch (err) {
      setError('Network error. Please check your connection and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.authContainer}>
      <h2 className={styles.authTitle}>Welcome Back</h2>
      <p className={styles.authSubtitle}>Sign in to continue learning</p>

      <form onSubmit={handleSubmit} className={styles.authForm}>
        <div className={styles.formGroup}>
          <label htmlFor="email" className={styles.label}>
            Email
          </label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className={styles.input}
            placeholder="your@email.com"
            required
            disabled={isLoading}
            autoComplete="email"
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="password" className={styles.label}>
            Password
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={styles.input}
            placeholder="Your password"
            required
            disabled={isLoading}
            autoComplete="current-password"
          />
        </div>

        {error && <div className={styles.error}>{error}</div>}

        <button
          type="submit"
          className={styles.submitButton}
          disabled={isLoading}
        >
          {isLoading ? 'Signing In...' : 'Sign In'}
        </button>
      </form>

      <p className={styles.switchText}>
        Don't have an account?{' '}
        <button
          type="button"
          onClick={onSwitchToSignup}
          className={styles.linkButton}
        >
          Create Account
        </button>
      </p>
    </div>
  );
}
