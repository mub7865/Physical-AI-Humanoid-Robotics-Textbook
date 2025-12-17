// T029: Layout with AuthProvider
import React from 'react';
import Layout from '@theme-original/Layout';
import { AuthProvider } from '../../context/AuthContext';
import ChatKitWidget from '../ChatKitWidget';
import AuthButtons from '../../components/AuthButtons';

export default function LayoutWrapper(props) {
  return (
    <AuthProvider>
      <Layout {...props}>
        {props.children}
      </Layout>
      <AuthButtons />
      <ChatKitWidget />
    </AuthProvider>
  );
}