import queue
import sys
import sounddevice as sd
import numpy as np
import torch
import torchaudio
from df.enhance import enhance, init_df

def main():
    print("[DNS] Khởi tạo model DeepFilterNet...")
    # Khởi tạo model và state. df_state chính là bộ nhớ để xử lý realtime mượt mà
    model, df_state, _ = init_df()
    
    SR = 48000
    # Blocksize 480 tương đương 10ms ở 48kHz. 
    # Đây là kích thước chunk lý tưởng để DeepFilterNet không bị méo tiếng do thiếu frame.
    BLOCKSIZE = 480
    
    # Hàng đợi (Queue) để giao tiếp giữa luồng thu âm và luồng xử lý
    audio_queue = queue.Queue()
    
    raw_frames = []
    denoised_frames = []

    def audio_callback(indata, frames, time, status):
        """Hàm này được gọi liên tục mỗi khi Mic thu đủ 480 samples"""
        if status:
            print(f"[Cảnh báo Audio] {status}", file=sys.stderr)
        # Bắn dữ liệu thô vào hàng đợi rồi thoát ngay để Mic không bị block
        audio_queue.put(indata.copy())

    print(f"\n[Sensory] Bắt đầu thu âm Real-time (Blocksize: {BLOCKSIZE} samples/10ms)...")
    print(">>> HÃY NÓI GÌ ĐÓ VÀ NHẤN Ctrl+C ĐỂ DỪNG/LƯU FILE <<<")

    try:
        # Mở luồng thu âm không đồng bộ (Asynchronous InputStream)
        with sd.InputStream(samplerate=SR, channels=1, dtype='float32', 
                            blocksize=BLOCKSIZE, callback=audio_callback):
            while True:
                # 1. Lấy chunk âm thanh thô từ hàng đợi (chờ nếu chưa có)
                indata = audio_queue.get()
                raw_frames.append(indata)

                # 2. Chuyển đổi sang Tensor [1, samples] cho DFN
                audio_tensor = torch.from_numpy(indata).T
                
                # 3. Lọc nhiễu Real-time (df_state được tự động cập nhật bên trong)
                enhanced_tensor = enhance(model, df_state, audio_tensor)
                
                # 4. Đẩy kết quả sạch vào mảng lưu trữ
                denoised_frames.append(enhanced_tensor.squeeze(0).numpy())
                
    except KeyboardInterrupt:
        print("\n[Sensory] Đã nhận lệnh dừng (Ctrl+C). Đang tiến hành lưu file...")

    # Hợp nhất các chunk lại thành file hoàn chỉnh
    if raw_frames and denoised_frames:
        # Nối các mảng lại với nhau và ép xẹp (squeeze) chiều kênh thừa
        # raw_audio_full ban đầu là [N, 1] -> squeeze thành [N]
        raw_audio_full = np.concatenate(raw_frames, axis=0).squeeze()
        denoised_audio_full = np.concatenate(denoised_frames, axis=0).squeeze()

        # Chuyển về Pytorch Tensor và thêm đúng 1 chiều kênh ở đầu -> [1, N] (2D Tensor)
        raw_tensor_save = torch.from_numpy(raw_audio_full).unsqueeze(0)
        denoised_tensor_save = torch.from_numpy(denoised_audio_full).unsqueeze(0)

        # Lưu xuống đĩa
        torchaudio.save("realtime_raw.wav", raw_tensor_save, SR)
        torchaudio.save("realtime_denoised.wav", denoised_tensor_save, SR)

        print("\n[IO] Đã lưu thành công 2 file audio!")
        print(" -> realtime_raw.wav")
        print(" -> realtime_denoised.wav")
    else:
        print("[Cảnh báo] Không có dữ liệu âm thanh nào được thu.")

if __name__ == "__main__":
    main()