// AuthButtons - Injects auth buttons into navbar
import React, { useState, useEffect, useRef, useCallback } from 'react';
import { createPortal } from 'react-dom';
import { useAuth } from '../../context/AuthContext';
import styles from './AuthButtons.module.css';

export default function AuthButtons() {
  const { user, isAuthenticated, isLoading, logout } = useAuth();
  const [navbarRight, setNavbarRight] = useState<Element | null>(null);
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  // Find navbar and keep checking on route changes
  const findNavbar = useCallback(() => {
    const navbar = document.querySelector('.navbar__items--right');
    if (navbar && navbar !== navbarRight) {
      setNavbarRight(navbar);
    }
  }, [navbarRight]);

  useEffect(() => {
    findNavbar();
    const observer = new MutationObserver(() => findNavbar());
    observer.observe(document.body, { childList: true, subtree: true });
    const interval = setInterval(findNavbar, 1000);
    return () => {
      observer.disconnect();
      clearInterval(interval);
    };
  }, [findNavbar]);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleLogout = async () => {
    setIsOpen(false);
    await logout();
    window.location.href = '/Physical-AI-Humanoid-Robotics-Textbook/';
  };

  if (!navbarRight || isLoading) {
    return null;
  }

  // Get user name - only show if it's a real string value
  const displayName = (user?.name && typeof user.name === 'string' && user.name !== 'string')
    ? user.name
    : 'User';

  // Get user email
  const displayEmail = (user?.email && typeof user.email === 'string')
    ? user.email
    : '';

  // Get initials
  const getInitials = () => {
    if (user?.name && typeof user.name === 'string' && user.name !== 'string') {
      return user.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    }
    if (user?.email && typeof user.email === 'string') {
      return user.email[0].toUpperCase();
    }
    return 'U';
  };

  const content = isAuthenticated && user ? (
    <div className={styles.container} ref={menuRef}>
      <button
        className={styles.avatarBtn}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="User menu"
      >
        <div className={styles.avatar}>{getInitials()}</div>
      </button>

      {isOpen && (
        <div className={styles.dropdown}>
          <div className={styles.userInfo}>
            <div className={styles.userName}>{displayName}</div>
            <div className={styles.userEmail}>{displayEmail}</div>
          </div>
          <hr className={styles.divider} />
          <button className={styles.logoutBtn} onClick={handleLogout}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
              <polyline points="16 17 21 12 16 7" />
              <line x1="21" y1="12" x2="9" y2="12" />
            </svg>
            Logout
          </button>
        </div>
      )}
    </div>
  ) : (
    <div className={styles.authBtns}>
      <a href="/Physical-AI-Humanoid-Robotics-Textbook/login" className={styles.signInBtn}>
        Sign In
      </a>
      <a href="/Physical-AI-Humanoid-Robotics-Textbook/signup" className={styles.signUpBtn}>
        Sign Up
      </a>
    </div>
  );

  return createPortal(content, navbarRight);
}
