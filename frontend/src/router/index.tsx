/* React Router configuration */

import { createBrowserRouter } from 'react-router-dom';
import MainLayout from '../components/layout/MainLayout';
import DashboardPage from '../pages/DashboardPage';
import DocumentsPage from '../pages/DocumentsPage';
import KnowledgeGraphPage from '../pages/KnowledgeGraphPage';
import ChatPage from '../pages/ChatPage';
import CompliancePage from '../pages/CompliancePage';
import MaintenancePage from '../pages/MaintenancePage';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: 'documents', element: <DocumentsPage /> },
      { path: 'knowledge-graph', element: <KnowledgeGraphPage /> },
      { path: 'chat', element: <ChatPage /> },
      { path: 'compliance', element: <CompliancePage /> },
      { path: 'maintenance', element: <MaintenancePage /> },
    ],
  },
]);
