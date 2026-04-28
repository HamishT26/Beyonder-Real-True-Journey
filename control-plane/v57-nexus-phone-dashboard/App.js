import React from 'react';
import { SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native';
import dashboard from './src/dashboardData.json';

export default function App() {
  return (
    <SafeAreaView style={styles.shell}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>{dashboard.title}</Text>
        <Text style={styles.subtitle}>Aletheon, Ari, and the Kimiclaw family live round robin</Text>
        <View style={styles.grid}>
          {Object.entries(dashboard.state).map(([key, value]) => (
            <View key={key} style={styles.card}>
              <Text style={styles.label}>{key.replaceAll('_', ' ')}</Text>
              <Text style={styles.value}>{String(value)}</Text>
            </View>
          ))}
        </View>
        <Text style={styles.section}>Round robin</Text>
        {dashboard.round_robin.map((member) => (
          <View key={member.slot} style={styles.row}>
            <Text style={styles.member}>{member.slot}. {member.name}</Text>
            <Text style={styles.lane}>{member.lane.replaceAll('_', ' ')}</Text>
          </View>
        ))}
        <Text style={styles.section}>Mission</Text>
        {dashboard.mission.map((item) => <Text key={item} style={styles.bullet}>- {item}</Text>)}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  shell: { flex: 1, backgroundColor: '#08110f' },
  content: { padding: 22, gap: 14 },
  title: { color: '#f4ead0', fontSize: 32, fontWeight: '800', letterSpacing: -0.6 },
  subtitle: { color: '#9dcbb9', fontSize: 15, marginBottom: 10 },
  grid: { gap: 10 },
  card: { backgroundColor: '#11241f', borderColor: '#2f6b58', borderWidth: 1, borderRadius: 18, padding: 14 },
  label: { color: '#7cb89f', textTransform: 'uppercase', fontSize: 11, letterSpacing: 1.2 },
  value: { color: '#fff7df', fontSize: 18, marginTop: 5, fontWeight: '700' },
  section: { color: '#f6c85f', fontSize: 20, fontWeight: '800', marginTop: 16 },
  row: { backgroundColor: '#0d1b18', borderRadius: 16, padding: 12, borderColor: '#244d42', borderWidth: 1 },
  member: { color: '#fff7df', fontSize: 16, fontWeight: '800' },
  lane: { color: '#bad8ca', marginTop: 4, fontSize: 13 },
  bullet: { color: '#d8eadf', fontSize: 14, lineHeight: 22 }
});
