import torch
import torch.nn as nn

# torch.cuda.is_available() checks and returns a Boolean True if a GPU is available, else it'll return False
is_cuda = torch.cuda.is_available()

# If we have a GPU available, we'll set our device to GPU. We'll use this device variable later in our code.
if is_cuda:
    device = torch.device("cuda")
else:
    device = torch.device("cpu")


## Two Models will be trained LSTM and Deep Neural
class LSTMmodel(nn.Module):

    def __init__(self, input, hidden_units, seq_len, pred_len):
        super(LSTMmodel, self).__init__()
        ## Batch First ensures input to be of shape (batch, seq, input)
        self.lstm1 = nn.LSTM(input, hidden_units, num_layers=1, batch_first=True)
        self.lstm2 = nn.LSTM(hidden_units, hidden_units, num_layers=1, batch_first=True)
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()
        self.dense1 = nn.Linear(in_features=hidden_units * seq_len, out_features=128)
        self.dense2 = nn.Linear(in_features=128, out_features=pred_len)

        self.input = input
        self.hidden_units = hidden_units
        self.seq_len = seq_len
        self.pred_len = pred_len

    # init_hidden()

    def init_hidden(self, batch_size):
        self.batch_size = batch_size
        self.hidden_state1 = (
        torch.zeros(1, self.batch_size, self.hidden_units), torch.zeros(1, self.batch_size, self.hidden_units))
        self.hidden_state2 = (
        torch.zeros(1, self.batch_size, self.hidden_units), torch.zeros(1, self.batch_size, self.hidden_units))

    def forward(self, x):
        ## x is of shape (batch, dims)
        # print(x.shape)
        x = x.reshape(self.batch_size, self.seq_len, -1)
        ## x of shape (batch, seq, input)
        # print(x.shape)
        out1, self.hidden_state1 = self.lstm1(x, self.hidden_state1)
        out1 = self.relu(out1)
        out2, self.hidden_state2 = self.lstm2(out1, self.hidden_state2)
        out2 = self.relu(out2)
        # print(out2.shape, self.batch_size)
        out3 = self.dense1(out2.reshape(self.batch_size, -1))
        out3 = self.relu(out3)
        out4 = self.dense2(out3)
        # arous = self.dense2(out2.reshape(self.batch_size, -1))
        ## Sets output to value -1, 1
        result = self.tanh(out4)
        # temp = temp.unsqueeze(dim=2)
        # humid = humid.unsqueeze(dim=2)

        return result


## Model for Densely connected Neural Networks
class NeuralModel(nn.Module):

    def __init__(self, input):
        super(NeuralModel, self).__init__()
        self.dense1 = nn.Linear(in_features=input, out_features=128)
        self.dense2 = nn.Linear(in_features=128, out_features=16)
        self.dense3 = nn.Linear(in_features=16, out_features=2)
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()

    def forward(self, x):
        out1 = self.dense1(x)
        out1 = self.relu(out1)
        out2 = self.dense2(out1)
        out2 = self.relu(out2)
        out3 = self.dense3(out2)
        ## Tanh activation for values from -1 to 1
        result = self.tanh(out3)

        return result


class RNNmodel_new(nn.Module):
    def __init__(self, input_size=28):
        super(RNNmodel, self).__init__()

        self.rnn = nn.LSTM(
            input_size=input_size,
            hidden_size=64,
            num_layers=1,
            batch_first=True,
        )
        self.out = nn.Linear(64, 10)

    def forward(self, x):
        r_out, (_, _) = self.rnn(x, None)
        out = self.out(r_out[:, -1, :])
        return out

class RNNmodel(nn.Module):
    def __init__(self, input_size, output_size, hidden_dim, n_layers, seq_size = 1):
        super(RNNmodel, self).__init__()

        # Defining some parameters
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

        # Defining the layers
        # RNN Layer
        # batch_first: If ``True``, then the input and output tensors are provided
        #             as `(batch, seq, feature)`. Default: ``False``
        # num_layers: Number of recurrent layers. E.g., setting ``num_layers=2``
        #             would mean stacking two RNNs together to form a `stacked RNN`,
        #             with the second RNN taking in outputs of the first RNN and
        #             computing the final results. Default: 1
        # input_size: The number of expected features in the input `x`
        # hidden_dim: The number of features in the hidden state `h`
        self.rnn = nn.RNN(input_size, hidden_dim, n_layers, batch_first=True, nonlinearity='relu', bidirectional=1)
        # Fully connected layer
        self.fc = nn.Linear(hidden_dim, output_size)

    def forward(self, x):
        print('line 108 forward (model)',x)
        batch_size = x.size(0)
        # batch_size = 1
        print('line 110 batch_size (model)', batch_size)
        # Initializing hidden state for first input using method defined below
        hidden = self.init_hidden(batch_size)
        print('line 113 hidden (model)', hidden.shape)
        # Passing in the input and hidden state into the model and obtaining outputs
        out, hidden = self.rnn(x, hidden)
        # Reshaping the outputs such that it can be fit into the fully connected layer
        out = out.contiguous().view(-1, self.hidden_dim)
        out = self.fc(out)

        return out, hidden

    def init_hidden(self, batch_size):
        # This method generates the first hidden state of zeros which we'll use in the forward pass
        # hidden = torch.zeros(self.n_layers, self.hidden_dim).to(device)
        hidden = torch.zeros(self.n_layers, batch_size, self.hidden_dim).to(device)
        # We'll send the tensor holding the hidden state to the device we specified earlier as well
        # print('hidden shape',hidden.shape)
        # exit()
        return hidden


class GRUmodel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, n_layers, drop_prob=0.2):
        super(GRUmodel, self).__init__()
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

        self.gru = nn.GRU(input_dim, hidden_dim, n_layers, batch_first=True, dropout=drop_prob)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.relu = nn.ReLU()

    def forward(self, x, h):
        out, h = self.gru(x, h)
        out = self.fc(self.relu(out[:, -1]))
        return out, h

    def init_hidden(self, batch_size):
        weight = next(self.parameters()).data
        hidden = weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(device)
        return hidden


class LSTMNet(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, n_layers, drop_prob=0.2):
        super(LSTMNet, self).__init__()
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

        self.lstm = nn.LSTM(input_dim, hidden_dim, n_layers, batch_first=True, dropout=drop_prob)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.relu = nn.ReLU()

    def forward(self, x, h):
        out, h = self.lstm(x, h)
        out = self.fc(self.relu(out[:, -1]))
        return out, h

    def init_hidden(self, batch_size):
        weight = next(self.parameters()).data
        hidden = (weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(device),
                  weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(device))
        return hidden
