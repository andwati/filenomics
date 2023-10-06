function toggleCustomFilename() {
    var preserveFilenameCheckbox = document.getElementById("preserve_filename");
    var customFilenameInput = document.getElementById("custom_filename");

    customFilenameInput.disabled = preserveFilenameCheckbox.checked;

    if (preserveFilenameCheckbox.checked) {
        customFilenameInput.value = "";
    }
}
