import torch
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

def get_mnist_loaders(batch_size=64, validation_split=0.1):
    """
    Downloads the MNIST dataset and prepares train, validation, and test DataLoaders.

    Args:
        batch_size (int): The number of samples per batch.
        validation_split (float): The fraction of the training data to use for validation.

    Returns:
        tuple: (train_loader, val_loader, test_loader)
    """
    
    # 1. Define the transformation pipeline
    # ToTensor() converts the PIL Image [0, 255] to a PyTorch Tensor [0.0, 1.0]
    # Normalize() shifts the mean and standard deviation of the data.
    # (0.1307,) and (0.3081,) are the pre-calculated mean and std for the MNIST dataset.
    # This helps the model train more efficiently.
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    # 2. Download the full training dataset
    train_dataset_full = datasets.MNIST(
        root='./data', 
        train=True, 
        download=True, 
        transform=transform
    )

    # 3. Download the test dataset
    test_dataset = datasets.MNIST(
        root='./data', 
        train=False, 
        download=True, 
        transform=transform
    )

    # 4. Split the full training dataset into a new (smaller) training set and a validation set
    num_train = len(train_dataset_full)
    split = int(num_train * validation_split)
    val_size = split
    train_size = num_train - val_size

    train_dataset, val_dataset = random_split(train_dataset_full, [train_size, val_size])

    # 5. Create the DataLoaders
    # DataLoader is a PyTorch utility that turns our Dataset into a generator.
    # It handles batching, shuffling, and multi-threaded data loading for us.
    
    # shuffle=True is critical for the training set to ensure the model
    # sees data in a different order every epoch, which prevents it from
    # learning the order of the data.
    train_loader = DataLoader(
        dataset=train_dataset,
        batch_size=batch_size,
        shuffle=True
    )

    # No shuffle is needed for validation or testing, as we are only
    # evaluating the model, not learning from it.
    val_loader = DataLoader(
        dataset=val_dataset,
        batch_size=batch_size,
        shuffle=False
    )

    test_loader = DataLoader(
        dataset=test_dataset,
        batch_size=batch_size,
        shuffle=False
    )

    print(f"Data successfully loaded.")
    print(f"Total training samples: {len(train_dataset)}")
    print(f"Total validation samples: {len(val_dataset)}")
    print(f"Total test samples: {len(test_dataset)}")
    
    return train_loader, val_loader, test_loader

if __name__ == '__main__':
    # You can run this file directly to test if the download works
    train_loader, _, _ = get_mnist_loaders(batch_size=32)
    print("\nTesting the loader...")
    images, labels = next(iter(train_loader))
    print(f"Batch of images shape: {images.shape}")
    print(f"Batch of labels shape: {labels.shape}")