from pathlib import Path
from typing import Dict, List
import os
import sys
import time

import numpy as np
import pandas as pd
import openai
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
STATIC_ROOT = os.path.join(BASE_DIR, "static")
sys.path.append(f"{BASE_DIR}/model")


class SyntheticGenerator:
    def __init__(
        self,
        topics_path: str = "data/topics.txt",
        starters_path: str = "data/starters.txt",
        df_path: str = "data/synthetic_chatgpt.csv",
        model_name: str = "gpt-3.5-turbo"
    ):
        self.topics_path = topics_path
        self.starters_path = starters_path
        self.df_path = df_path
        self.model_name = model_name

        self.topics = None
        self.starters = None
        self.generated_count = 0

        self.setup()

    def setup(self):
        self._load_topics()
        self._load_starters()
        self._init_dataframe()

    def _load_topics(self) -> None:
        """
            Load prompts topics from the csv file
        """
        with open(self.topics_path, 'r') as topics_file:
            self.topics = list(map(lambda x: x.strip(), topics_file.readlines()))

    def _load_starters(self) -> List[str]:
        """
            Load prompts starters from the txt file
        """
        with open(self.starters_path, 'r') as starters_file:
            self.starters = list(map(lambda x: x.strip(), starters_file.readlines()))

    def _create_prompt_message(self) -> List[Dict[str, str]]:
        """
            Create prompt message for the ChatGPT Api
        """
        random_topic = np.random.choice(self.topics, size=1)[0]
        random_starter = np.random.choice(self.starters, size=1)[0]

        prompt = random_starter.replace('{}', random_topic)
        prompt_message = [{"role": "user", "content": f"{prompt}"}]
        return prompt_message

    def _init_dataframe(self) -> None:
        """
            Initialize dataframe to store the generated texts
        """
        # If not the first time generating then read, else create
        if os.path.exists(self.df_path):
            self.df = pd.read_csv(self.df_path)
        else:
            self.df = pd.DataFrame(columns=['prompt', 'text', 'is_generated', 'generator'])
            self.df.to_csv(self.df_path, index=False)

    def _resave_dataframe(self, prompt: str, generated_text: str) -> None:
        text_row = {
            "prompt": prompt,
            "text": generated_text,
            "is_generated": 1,
            "generator": self.model_name
        }

        self.df.loc[len(self.df)] = text_row
        self.df.to_csv(self.df_path, index=False)

    def start_generating(self):
        """
            Main function to generate the texts
        """
        # Start generating endlessly
        for _ in range(500):
            print("Start generating...")
            start = time.time()

            random_prompt_message = self._create_prompt_message()
            # Get answer using openai API
            completion = openai.ChatCompletion.create(
                model=self.model_name,
                messages=random_prompt_message
            )

            # Get reply from dict completion
            prompt = random_prompt_message[0]['content']
            reply_content = completion.choices[0].message.content

            # Save the answer
            self._resave_dataframe(prompt, reply_content)

            self.generated_count += 1
            print(f"Time passed: {time.time() - start}")
            self.log(prompt, reply_content)
            time.sleep(np.random.randint(5, 50))

    def log(self, prompt: str, text: str):
        print(f"Generated: {self.generated_count}")
        print(f"Prompt: {prompt}")
        print(f"Text: {text}")
        print("#####################################")


if __name__ == "__main__":
    # Read .env file
    load_dotenv()

    # Set ChatGPT Api key
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # Start generating texts
    generator = SyntheticGenerator()
    generator.start_generating()
