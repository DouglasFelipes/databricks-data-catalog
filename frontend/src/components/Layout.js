import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Stack,
  Nav,
  CommandBar,
  Text,
  mergeStyleSets
} from '@fluentui/react';
import {
  HomeRegular,
  SearchRegular,
  ShieldTaskRegular
} from '@fluentui/react-icons';

const styles = mergeStyleSets({
  root: {
    height: '100vh',
    display: 'flex',
    flexDirection: 'column',
    background: '#faf9f8'
  },
  header: {
    background: '#ffffff',
    borderBottom: '1px solid #edebe9',
    padding: '0 24px',
    height: '48px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between'
  },
  logo: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px'
  },
  logoIcon: {
    fontSize: '24px'
  },
  logoText: {
    fontSize: '16px',
    fontWeight: '600',
    color: '#323130'
  },
  container: {
    display: 'flex',
    flex: 1,
    overflow: 'hidden'
  },
  sidebar: {
    width: '240px',
    background: 'linear-gradient(180deg, #0078d4 0%, #106ebe 100%)',
    padding: '16px 0',
    boxShadow: '2px 0 4px rgba(0,0,0,0.08)'
  },
  content: {
    flex: 1,
    overflow: 'auto',
    padding: '24px'
  }
});

const Layout = ({ children }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const navLinkGroups = [
    {
      links: [
        {
          name: 'Dashboard',
          url: '/',
          key: 'dashboard',
          icon: 'Home'
        },
        {
          name: 'Explorer',
          url: '/explorer',
          key: 'explorer',
          icon: 'Search'
        },
        {
          name: 'Quality',
          url: '/quality',
          key: 'quality',
          icon: 'ShieldTask'
        }
      ]
    }
  ];

  const commandBarItems = [
    {
      key: 'refresh',
      text: 'Refresh',
      iconProps: { iconName: 'Refresh' },
      onClick: () => window.location.reload()
    }
  ];

  return (
    <div className={styles.root}>
      {/* Top Command Bar */}
      <div className={styles.header}>
        <div className={styles.logo}>
          <span className={styles.logoIcon}>🎯</span>
          <Text className={styles.logoText}>Data Governance Portal</Text>
        </div>
        <CommandBar
          items={commandBarItems}
          styles={{
            root: {
              padding: 0,
              background: 'transparent'
            }
          }}
        />
      </div>

      <div className={styles.container}>
        {/* Left Navigation */}
        <div className={styles.sidebar}>
          <Nav
            groups={navLinkGroups}
            selectedKey={location.pathname === '/' ? 'dashboard' : location.pathname.substring(1)}
            onLinkClick={(ev, item) => {
              ev?.preventDefault();
              navigate(item.url);
            }}
            styles={{
              root: {
                width: '100%'
              },
              link: {
                color: 'rgba(255,255,255,0.9)',
                padding: '12px 24px',
                selectors: {
                  ':hover': {
                    background: 'rgba(255,255,255,0.1)',
                    color: '#ffffff'
                  },
                  '.is-selected': {
                    background: '#ffffff',
                    color: '#0078d4'
                  }
                }
              },
              linkText: {
                fontSize: '14px',
                fontWeight: '500'
              }
            }}
          />
        </div>

        {/* Main Content */}
        <div className={styles.content}>
          {children}
        </div>
      </div>
    </div>
  );
};

export default Layout;
