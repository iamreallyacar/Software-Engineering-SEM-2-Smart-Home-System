/**
 * Dashboard page - placeholder for now
 */

import React from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Button,
} from '@mui/material';
import {
  Home as HomeIcon,
  ExitToApp as LogoutIcon,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const DashboardPage: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        {/* Header */}
        <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <HomeIcon sx={{ fontSize: 32, color: 'primary.main', mr: 2 }} />
              <Typography variant="h4" component="h1">
                Smart Home Dashboard
              </Typography>
            </Box>
            <Button
              variant="outlined"
              startIcon={<LogoutIcon />}
              onClick={handleLogout}
            >
              Logout
            </Button>
          </Box>
          <Typography variant="h6" color="text.secondary" sx={{ mt: 1 }}>
            Welcome back, {user?.username}!
          </Typography>
        </Paper>

        {/* Content */}
        <Paper elevation={1} sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h5" gutterBottom>
            🏠 Dashboard Coming Soon!
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            Your smart home dashboard is being built with amazing features:
          </Typography>
          
          <Box sx={{ textAlign: 'left', maxWidth: 600, mx: 'auto' }}>
            <Typography variant="body2" sx={{ mb: 1 }}>
              ⚡ Real-time energy monitoring and consumption tracking
            </Typography>
            <Typography variant="body2" sx={{ mb: 1 }}>
              🏡 Smart home and room management
            </Typography>
            <Typography variant="body2" sx={{ mb: 1 }}>
              📱 Device control with instant feedback
            </Typography>
            <Typography variant="body2" sx={{ mb: 1 }}>
              🎭 Demo scenarios for automation
            </Typography>
            <Typography variant="body2" sx={{ mb: 1 }}>
              💡 Energy efficiency tips and recommendations
            </Typography>
            <Typography variant="body2" sx={{ mb: 1 }}>
              📊 Interactive charts and analytics
            </Typography>
          </Box>

          <Box sx={{ mt: 4, p: 3, bgcolor: 'primary.light', borderRadius: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              🚀 Next Steps
            </Typography>
            <Typography variant="body2">
              The authentication system is now working! Next, we'll add:
              <br />• Smart home creation and management
              <br />• Real-time device control interface
              <br />• Energy dashboard with live data
              <br />• Demo scenarios integration
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default DashboardPage;
