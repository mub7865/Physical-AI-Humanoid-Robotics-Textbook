import React from 'react';
import Layout from '@theme-original/Layout';
import ChatWidget from '../ChatWidget';

export default function LayoutWrapper(props) {
  return (
    <>
      <Layout {...props}>
        {props.children}
      </Layout>
      <ChatWidget />
    </>
  );
}