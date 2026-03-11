import React from 'react';
import { Stack, Text, mergeStyleSets } from '@fluentui/react';

const styles = mergeStyleSets({
  card: {
    background: '#ffffff',
    borderRadius: '8px',
    padding: '24px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.08)',
    border: '1px solid #edebe9',
    position: 'relative',
    overflow: 'hidden',
    transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
    selectors: {
      ':hover': {
        transform: 'translateY(-4px)',
        boxShadow: '0 8px 24px rgba(0,120,212,0.15)'
      },
      '::before': {
        content: '""',
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        height: '4px',
        background: 'linear-gradient(90deg, #0078d4, #50e6ff)'
      }
    }
  },
  icon: {
    fontSize: '32px',
    marginBottom: '12px'
  },
  value: {
    fontSize: '40px',
    fontWeight: '700',
    color: '#0078d4',
    lineHeight: '1',
    marginBottom: '8px'
  },
  label: {
    fontSize: '12px',
    color: '#605e5c',
    fontWeight: '600',
    textTransform: 'uppercase',
    letterSpacing: '0.5px'
  },
  trend: {
    fontSize: '12px',
    marginTop: '8px',
    fontWeight: '500'
  },
  trendPositive: {
    color: '#107c10'
  },
  trendNegative: {
    color: '#d13438'
  }
});

const KPICard = ({ icon, value, label, trend, trendPositive }) => {
  return (
    <div className={styles.card}>
      <Stack tokens={{ childrenGap: 4 }}>
        <span className={styles.icon}>{icon}</span>
        <Text className={styles.value}>{value}</Text>
        <Text className={styles.label}>{label}</Text>
        {trend && (
          <Text className={`${styles.trend} ${trendPositive ? styles.trendPositive : styles.trendNegative}`}>
            {trendPositive ? '↑' : '↓'} {trend}
          </Text>
        )}
      </Stack>
    </div>
  );
};

export default KPICard;
