from keras import layers
from keras import models
from keras import optimizers
import keras.backend as K

class Critic:
    """Critic (Value) Model."""
    def __init__(self, state_size, action_size, learning_rate=1e-3):
        """Initialize parameters and build model.

        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
        """
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        
        # Initialize any other variables here

        self.build_model()

    def build_model(self):
        """Build a critic (value) network that maps (state, action) pairs -> Q-values."""
        # Define input layers
        states = layers.Input(shape=(self.state_size,), name='states')
        actions = layers.Input(shape=(self.action_size,), name='actions')

#         dropout_rate = 0.05
        
        # Add hidden layer(s) for state pathway
        net_states = layers.Dense(units=32, activation='relu')(states)
#         net_states = layers.BatchNormalization()(net_states)
#         net_states = layers.Dropout(dropout_rate)(net_states)
        
        net_states = layers.Dense(units=64, activation='relu')(net_states)
#         net_states = layers.BatchNormalization()(net_states)
#         net_states = layers.Dropout(dropout_rate)(net_states)

        # Add hidden layer(s) for action pathway
        net_actions = layers.Dense(units=32, activation='relu')(actions)
#         net_actions = layers.BatchNormalization()(net_actions)
#         net_actions = layers.Dropout(dropout_rate)(net_actions)
        
        net_actions = layers.Dense(units=64, activation='relu')(net_actions)
#         net_actions = layers.BatchNormalization()(net_actions)
#         net_actions = layers.Dropout(dropout_rate)(net_actions)

        # Try different layer sizes, activations, add batch normalization, regularizers, etc.

        # Combine state and action pathways
        net = layers.Add()([net_states, net_actions])
        net = layers.Activation('relu')(net)
#         net = layers.BatchNormalization()(net)
#         net = layers.Dropout(dropout_rate)(net)

        # Add more layers to the combined network if needed
        net = layers.Dense(units=256, activation='relu')(net)
#         net = layers.BatchNormalization()(net)
#         net = layers.Dropout(dropout_rate)(net)

        # Add final output layer to prduce action values (Q values)
        Q_values = layers.Dense(units=1, name='q_values')(net)

        # Create Keras model
        self.model = models.Model(inputs=[states, actions], outputs=Q_values)

        # Define optimizer and compile model for training with built-in loss function
        optimizer = optimizers.Adam(lr=self.learning_rate)
        self.model.compile(optimizer=optimizer, loss='mse')

        # Compute action gradients (derivative of Q values w.r.t. to actions)
        action_gradients = K.gradients(Q_values, actions)

        # Define an additional function to fetch action gradients (to be used by actor model)
        self.get_action_gradients = K.function(
            inputs=[*self.model.input, K.learning_phase()],
            outputs=action_gradients)
