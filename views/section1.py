def section1():
    # Pass the data to the HTML template (View)
    ground_truth_url = "xxyz"
    classification_output_url = "xxyz"
    ewma_accuracy_url = "52%"

    return {
        'ground_truth_url': ground_truth_url,
        'classification_output_url': classification_output_url,
        'ewma_accuracy_url': ewma_accuracy_url
    }