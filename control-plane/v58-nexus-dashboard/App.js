import React from 'react';
import { SafeAreaView, ScrollView, Text, View } from 'react-native';
import data from './src/dashboardData.json';

export default function App() {
  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: '#07130f' }}>
      <ScrollView contentContainerStyle={{ padding: 24, gap: 14 }}>
        <Text style={{ color: '#f0c96a', letterSpacing: 2 }}>V58 OMEGA</Text>
        <Text style={{ color: '#f4fff8', fontSize: 34, fontWeight: '800' }}>{data.title}</Text>
        {['kubernetes_state', 'suite_ladder_state', 'notion_dashboard_state'].map((key) => (
          <View key={key} style={{ padding: 18, borderRadius: 18, backgroundColor: '#10251d' }}>
            <Text style={{ color: '#a9c9bb', textTransform: 'uppercase' }}>{key}</Text>
            <Text style={{ color: '#66f0a3', fontSize: 20 }}>{data[key]}</Text>
          </View>
        ))}
        <View style={{ padding: 18, borderRadius: 18, backgroundColor: '#10251d' }}>
          <Text style={{ color: '#a9c9bb', textTransform: 'uppercase' }}>Round Robin</Text>
          <Text style={{ color: '#f4fff8', fontSize: 18 }}>{data.members.join(' | ')}</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
