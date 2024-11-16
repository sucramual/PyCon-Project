# LLM Cantonese Response Comparison

A Streamlit application that lets users compare responses from different Large Language Models (LLMs) in Cantonese. Users can test their ability to identify which model generated which response.

## Features

- Interactive UI for comparing responses from multiple LLMs (GPT-4 and other models)
- Question selection interface
- Real-time scoring system
- Success rate tracking
- Randomized answer positioning for fair comparison


## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
export OPENAI_API_KEY=your_api_key_here
```

3. Run the application:
```bash
cd streamlit
streamlit run main.py
```

## Data Pipeline

1. **Data Collection**
   - `Scraper/scraper.py`: Scrapes restaurant data
   - Raw data stored in JSON format (`restaurants.json`, `restaurants_with_districts.json`)

2. **Data Processing**
   - `data_cleaning/`: Contains scripts for data preprocessing and manipulation
   - `qa_generators_v2.py`: Generates QA pairs for training and testing

3. **Model Outputs**
   - Various model outputs stored in `q_and_a/` directory
   - Generated outputs from different Qwen models in `generated_output/`

## Development

### Core Components

- `streamlit/`: Contains all UI-related code
  - `main.py`: Application entry point
  - `ui_components.py`: Reusable UI components
  - `data_handler.py`: Data loading and processing
  - `state_manager.py`: Manages application state

### Data Generation

The project includes comprehensive data processing pipeline:
- Restaurant data scraping
- Training/test data splitting
- QA pair generation
- Multiple model inference

### Models Used

- GPT-4
- Qwen-25-3B
- Qwen-25-15B
- Qwen-25-05B

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Feedback

Please submit any issues or suggestions via [Linkedin](https://www.linkedin.com/in/marcuslauyc/) or [Email](mailto:ylau36@gatech.edu)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Created for PyCon Hong Kong 2024