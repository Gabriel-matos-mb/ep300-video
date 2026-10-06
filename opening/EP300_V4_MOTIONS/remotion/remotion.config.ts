import path from 'node:path';
import {Config} from '@remotion/cli/config';

// assets (fontes, stickers, logos) ficam em ../assets para o Gabriel trocar sem abrir codigo
Config.setPublicDir(path.resolve(process.cwd(), '../assets'));
Config.setVideoImageFormat('png');
Config.setOverwriteOutput(true);
