import sounddevice as sd
import numpy as np
import torch
import torchaudio
import matplotlib.pyplot as plt
import sys
from df.enhance import enhance, init_df
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
def record_audio(duration: int, sr: int) -> torch.Tensor:
    """Thu âm từ microphone và trả về PyTorch Tensor [channels, samples]"""
    print(f"\n[Sensory] Bắt đầu thu âm {duration} giây...")
    print(">>> HÃY NÓI GÌ ĐÓ VÀ TẠO RA TIẾNG ỒN (gõ phím, bật quạt...) <<<")
    
    # Thu âm dạng float32, mono
    audio_np = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='float32')
    sd.wait()
    
    print("[Sensory] Thu âm hoàn tất!")
    # Chuyển đổi numpy array sang tensor [1, N]
    audio_tensor = torch.from_numpy(audio_np).T
    return audio_tensor

def plot_stft_spectrograms(raw_tensor, denoised_tensor, save_path="stft_spectrogram.png"):
    """Tính toán STFT và vẽ 2 ảnh phổ xếp chồng lên nhau"""
    print("[Vision] Đang tính toán và vẽ STFT Spectrogram...")
    
    # Cấu hình STFT
    n_fft = 1024
    hop_length = 256
    window = torch.hann_window(n_fft)

    def get_log_mag(tensor):
        # Tính STFT
        stft_out = torch.stft(
            tensor, 
            n_fft=n_fft, 
            hop_length=hop_length, 
            window=window, 
            return_complex=True
        )
        # Lấy biên độ (Magnitude) và chuyển sang thang Log
        mag = torch.abs(stft_out)
        log_mag = 20 * torch.log10(mag + 1e-9)
        return log_mag[0].numpy() # Lấy channel đầu tiên và chuyển về numpy

    log_stft_raw = get_log_mag(raw_tensor)
    log_stft_denoised = get_log_mag(denoised_tensor)

    # Thiết lập Matplotlib nền đen
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
    plt.subplots_adjust(hspace=0.2) # Khoảng cách giữa 2 ảnh

    # Vẽ Raw Audio
    ax1.imshow(log_stft_raw, origin='lower', aspect='auto', cmap='magma')
    ax1.axis('off') # Tắt toàn bộ trục hoành, trục tung, dB
    ax1.set_title("RAW AUDIO", color='white', fontweight='bold', pad=10)

    # Vẽ Denoised Audio
    ax2.imshow(log_stft_denoised, origin='lower', aspect='auto', cmap='magma')
    ax2.axis('off') # Tắt toàn bộ trục hoành, trục tung, dB
    ax2.set_title("DENOISED AUDIO", color='white', fontweight='bold', pad=10)
    save_path = Path("data/denoise/stft.png")
    # Lưu ảnh
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0.1, dpi=150)
    plt.close()
    print(f"[Vision] Đã lưu ảnh phổ tại: {save_path}")

def main():
    # Thông số cấu hình
    SR = 48000
    DURATION = 5

    # 1. Thu âm (Lớp Cảm Giác)
    raw_audio = record_audio(DURATION, SR)

    # 2. Khởi tạo DeepFilterNet
    print("\n[DNS] Đang khởi tạo model DeepFilterNet...")
    model, df_state, _ = init_df()

    # 3. Lọc nhiễu
    print("[DNS] Đang xử lý lọc nhiễu...")
    # DeepFilterNet nhận input là tensor [channels, samples]
    denoised_audio = enhance(model, df_state, raw_audio)
    raw_path = Path("data/denoise/raw_test.wav")
    raw_path.parent.mkdir(parents=True,exist_ok=True)
    denoised_path = Path("data/denoise/denoised_test.wav")
    # 4. Lưu file Wav để nghe thử
    torchaudio.save(str(raw_path), raw_audio, SR)
    torchaudio.save(str(denoised_path), denoised_audio, SR)
    print("\n[IO] Đã lưu 2 file audio:")
    print(" -> raw_test.wav")
    print(" -> denoised_test.wav")

    # 5. Vẽ và xuất ảnh STFT
    plot_stft_spectrograms(raw_audio, denoised_audio)
    
    print("\nHoàn tất bài test! Mời sếp mở thư mục lên kiểm tra hàng.")

if __name__ == "__main__":
    main()