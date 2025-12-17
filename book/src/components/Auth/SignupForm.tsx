// T018: SignupForm Component
import React, { useState } from 'react';
import styles from './Auth.module.css';

interface SignupFormProps {
  onSignupSuccess: (user: { id: string; email: string; name?: string }) => void;
  onSwitchToLogin: () => void;
}

// Live backend URL
const API_URL = 'https://physical-ai-humanoid-robotics-textb-one.vercel.app';

export default function SignupForm({ onSignupSuccess, onSwitchToLogin }: SignupFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Client-side validation
    if (password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
          name: name || undefined,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        if (data.detail?.error === 'EMAIL_EXISTS') {
          setError('This email is already registered. Please sign in instead.');
        } else if (data.detail?.error === 'WEAK_PASSWORD') {
          setError('Password must be at least 8 characters');
        } else {
          setError(data.detail?.message || 'Signup failed. Please try again.');
        }
        return;
      }

      // Signup successful - pass user data to parent
      onSignupSuccess({
        id: data.id,
        email: data.email,
        name: data.name,
      });
    } catch (err) {
      setError('Network error. Please check your connection and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.authContainer}>
      <h2 className={styles.authTitle}>Create Account</h2>
      <p className={styles.authSubtitle}>Join our robotics learning community</p>

      <form onSubmit={handleSubmit} className={styles.authForm}>
        <div className={styles.formGroup}>
          <label htmlFor="name" className={styles.label}>
            Name (optional)
          </label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className={styles.input}
            placeholder="Your name"
            disabled={isLoading}
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="email" className={styles.label}>
            Email *
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
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="password" className={styles.label}>
            Password *
          </label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={styles.input}
            placeholder="Minimum 8 characters"
            required
            minLength={8}
            disabled={isLoading}
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="confirmPassword" className={styles.label}>
            Confirm Password *
          </label>
          <input
            type="password"
            id="confirmPassword"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className={styles.input}
            placeholder="Confirm your password"
            required
            minLength={8}
            disabled={isLoading}
          />
        </div>

        {error && <div className={styles.error}>{error}</div>}

        <button
          type="submit"
          className={styles.submitButton}
          disabled={isLoading}
        >
          {isLoading ? 'Creating Account...' : 'Create Account'}
        </button>
      </form>

      <p className={styles.switchText}>
        Already have an account?{' '}
        <button
          type="button"
          onClick={onSwitchToLogin}
          className={styles.linkButton}
        >
          Sign In
        </button>
      </p>
    </div>
  );
}
