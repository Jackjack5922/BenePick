from data_pipeline.gov.gov24_data_pipeline import run_gov24_data_pipeline

if __name__ == "__main__":
    print("🚀 정부24 데이터 수집 및 통합 파이프라인 실행 시작...")
    try:
        run_gov24_data_pipeline()
        print("✅ 파이프라인 실행 완료.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")