import React from 'react';
import {Composition, registerRoot, AbsoluteFill} from 'remotion';
// CONTROLE NEGATIVO do QA de cobertura: mesma moldura dos slots, mas SEM fundo (deve produzir PNG com alfa < 255).
const Ctrl: React.FC = () => <AbsoluteFill><div style={{position: 'absolute', left: 100, top: 100, width: 300, height: 200, background: '#F47340'}} /></AbsoluteFill>;
registerRoot(() => <Composition id="QA-CONTROL" component={Ctrl} durationInFrames={10} fps={24000 / 1001} width={1920} height={1080} />);
