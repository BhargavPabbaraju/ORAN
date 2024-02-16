def section1():
    # Pass the data to the HTML template (View)
    ground_truth_url = "Ground Truth URL"
    classification_output_url = "Classification Output URL"
    ewma_accuracy_url = "52%"

    return {
        'ground_truth_url': ground_truth_url,
        'classification_output_url': classification_output_url,
        'ewma_accuracy_url': ewma_accuracy_url
    }