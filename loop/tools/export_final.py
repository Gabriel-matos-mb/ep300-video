import sys, subprocess, multiprocessing as mp
sys.path.insert(0, '.')
import build
O='out/'
cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','-','-filter_complex','[0:v]split=2[a][b];[b]scale=3840:2160:flags=lanczos[c]',
 '-map','[a]','-c:v','libx264','-preset','slow','-crf','14','-pix_fmt','yuv420p','-g','60','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart','-an',O+'EP300_LOOP_FINAL_1080p.mp4',
 '-map','[c]','-c:v','libx264','-preset','slow','-crf','15','-pix_fmt','yuv420p','-g','60','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart','-an',O+'EP300_LOOP_FINAL_4K.mp4']
if __name__=='__main__':
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    with mp.Pool(8,initializer=build._init) as pool:
        for i,raw in enumerate(pool.imap(build._job,range(build.N),chunksize=6)): p.stdin.write(raw)
    p.stdin.close(); p.wait(); print('ok')
