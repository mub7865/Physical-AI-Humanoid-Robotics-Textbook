// Custom DocItem/Content - Adds ContentToolbar for Personalization and Translation
import React, { useState } from 'react';
import clsx from 'clsx';
import { ThemeClassNames } from '@docusaurus/theme-common';
import { useDoc } from '@docusaurus/plugin-content-docs/client';
import Heading from '@theme/Heading';
import MDXContent from '@theme/MDXContent';
import ContentToolbar from '../../../components/ContentToolbar';
import type { Props } from '@theme/DocItem/Content';

// Title component
function DocTitle({ title }: { title: string }): JSX.Element {
  return (
    <Heading as="h1" className={clsx('doc-title', ThemeClassNames.docs.docTitle)}>
      {title}
    </Heading>
  );
}

// Simple markdown to HTML converter
function convertMarkdownToHtml(markdown: string): string {
  return markdown
    .replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^### (.*$)/gm, '<h3>$1</h3>')
    .replace(/^## (.*$)/gm, '<h2>$1</h2>')
    .replace(/^# (.*$)/gm, '<h1>$1</h1>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')
    .replace(/^\- (.*$)/gm, '<li>$1</li>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br />');
}

export default function DocItemContent({ children }: Props): JSX.Element {
  const { metadata, contentTitle } = useDoc();
  const [modifiedContent, setModifiedContent] = useState<string | null>(null);
  const [contentMode, setContentMode] = useState<'original' | 'personalized' | 'translated'>('original');

  // Extract text from DOM after render for API calls
  const getPageText = (): string => {
    if (typeof document === 'undefined') return '';
    const article = document.querySelector('article');
    return article?.innerText || '';
  };

  const handleContentChange = (newContent: string, type: 'original' | 'personalized' | 'translated') => {
    setContentMode(type);
    if (type === 'original') {
      setModifiedContent(null);
    } else {
      setModifiedContent(newContent);
    }
  };

  // Generate chapter ID from metadata
  const chapterId = metadata.id || metadata.slug || 'unknown';

  // Always show toolbar on doc pages
  const showToolbar = true;

  return (
    <div className={clsx(ThemeClassNames.docs.docMarkdown, 'markdown')}>
      {contentTitle && <DocTitle title={metadata.title} />}

      {showToolbar && (
        <ContentToolbar
          chapterId={chapterId}
          originalContent={getPageText()}
          onContentChange={handleContentChange}
        />
      )}

      {contentMode === 'original' || !modifiedContent ? (
        <MDXContent>{children}</MDXContent>
      ) : (
        <div
          className="modified-content markdown"
          dangerouslySetInnerHTML={{ __html: convertMarkdownToHtml(modifiedContent) }}
        />
      )}
    </div>
  );
}
