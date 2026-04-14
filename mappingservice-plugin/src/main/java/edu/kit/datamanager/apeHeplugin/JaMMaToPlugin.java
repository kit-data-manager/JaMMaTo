package edu.kit.datamanager.jammatoplugin;

import edu.kit.datamanager.mappingservice.plugins.AbstractPythonMappingPlugin;
import java.nio.file.Path;

public class JaMMaToPlugin extends AbstractPythonMappingPlugin{

    private static final String REPOSITORY = "https://github.com/kit-data-manager/JaMMaTo";


    public JaMMaToPlugin() {
        super("Dicom2JSON", REPOSITORY);
    }

    @Override
    public String name() {
        return "Dicom2JSON";
    }

    @Override
    public String description() {
        return "The software JaMMaTo (JSON Metadata Mapping Tool) is a metadata mapping tool based on Python and used for mapping metadata from a Dicom input to a JSON format schema. ";
    }

    @Override
    public String[] inputTypes() {
        return new String[]{
            "application/octet-stream", 
            "application/x-hdf5",
            "application/dicom",
            "application/x-iso9660-image"
        };
    }

    @Override
    public String[] outputTypes() {
        return new String[]{
            "application/json"
        };
    }

    @Override
    public String[] getCommandArray(Path workingDir, Path mappingFile, Path inputFile, Path outputFile) {
        return new String[]{
                workingDir + "/plugin_wrapper.py",
                "-m",
                mappingFile.toString(),
                "-i",
                inputFile.toString(),
                "-o",
                outputFile.toString()
        };
    }
}
