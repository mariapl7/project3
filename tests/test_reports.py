import pandas as pd
import pytest
from unittest import mock
from src.reports import load_data


@pytest.fixture
def sample_dataframe():
    data = {
        'Дата операции': ['2023-09-01', '2023-09-02'],
        'Дата платежа': ['2023-09-03', '2023-09-04'],
        'Сумма': [100.0, 200.0],
    }
    return pd.DataFrame(data)


@mock.patch('your_module.pd.read_excel')
@mock.patch('os.path.isfile')
def test_load_data_success(mock_isfile, mock_read_excel, sample_dataframe):
    mock_isfile.return_value = True
    mock_read_excel.return_value = sample_dataframe

    result = load_data('operations.xlsx')

    assert result is not None
    assert isinstance(result, pd.DataFrame)
    assert result.shape == (2, 3)
    assert result['Дата операции'].dtype == 'datetime64[ns]'
    assert result['Дата платежа'].dtype == 'datetime64[ns]'


@mock.patch('os.path.isfile')
def test_load_data_file_not_found(mock_isfile):
    mock_isfile.return_value = False

    result = load_data('non_existent_file.xlsx')

    assert result is None
