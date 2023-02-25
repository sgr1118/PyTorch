# -*- coding: utf-8 -*-
"""rnn

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XE_RORXsoNreGBriwkFKj-lE0HLuOCvB
"""

import torch
import torch.nn as nn

class SequenceClassifier(nn.Module):

    def __init__(
        self,
        input_size,
        hidden_size,
        output_size,
        n_layers=4,
        dropout_p=.2,
    ):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.n_layers = n_layers
        self.dropout_p = dropout_p

        super().__init__()

        # LSTM 클래스 객체를 생성하여 RNN에 할당
        self.rnn = nn.LSTM(
            input_size = input_size,
            hidden_size = hidden_size,
            num_layers = n_layers, # 다계층
            batch_first = True, # batch_firstfmf True로 설정하는 이유는는 아래 참고
            dropout = dropout_p, # LSTM 내부 계층 사이사이에 드롭아웃을 넣어주도록한다.
            bidirectional = True, # 양방향
        )
        # self.layers 변수에 하래 객체를 할당한다.
        self.layers = nn.Sequential( 
            nn.ReLU(), # 활성화 함수
            nn.BatchNorm1d(hidden_size * 2), # 배치정규화
            nn.Linear(hidden_size * 2, output_size), # 선형 계층
            nn.LogSoftmax(dim=-1) # 로그 소프트맥스 계층
        )

    # init 메서드에서 생성된 객체들을 활용하여 연산을 수행
    # 다대일 형태를 문제를 다루므로 출력 텐서만 활용
    def forward(self, x): 
        # |x| = (batch_size, h, w)
        z, _ = self.rnn(x) # 입력 텐서 x 삽입
        # |z| = (batch_size, h, hidden_size * 2)
        z = z[:, -1] # 출력 텐서만 활용
        # |z| = (batch_size, hidden_size * 2)
        y = self.layers(z)
        # |y| = (batch_size, output_size)

        return y