#include <cstdio>
#include <string>
#include <iostream>
#include <sstream>
#include <fstream>

#include <map>
#include <utility>
#include <set>

#include "clang/AST/ASTConsumer.h"
#include "clang/AST/RecursiveASTVisitor.h"
#include "clang/Basic/Diagnostic.h"
#include "clang/Basic/FileManager.h"
#include "clang/Basic/SourceManager.h"
#include "clang/Basic/TargetOptions.h"
#include "clang/Basic/TargetInfo.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Lex/Preprocessor.h"
#include "clang/Parse/ParseAST.h"
#include "clang/Rewrite/Core/Rewriter.h"
#include "clang/Rewrite/Frontend/Rewriters.h"
#include "llvm/Support/Host.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/ADT/IntrusiveRefCntPtr.h"
#include "clang/Lex/HeaderSearch.h"
#include "clang/Frontend/Utils.h"
#include "clang/Tooling/Tooling.h"
#include "clang/Frontend/CompilerInstance.h"
// #include "clang/Frontend/FrontendAction.h"

using namespace clang;
using namespace std;


class MyASTVisitor : public RecursiveASTVisitor<MyASTVisitor>
{
public:
    MyASTVisitor(
        Rewriter &R,
        const LangOptions &langOptions,
        SourceManager &sourceManager,
        Lexer &lexer,
        set<FileID> &modified_file_ids
    )
        : TheRewriter(R),
        LangOpts(langOptions),
        m_sourceManager(sourceManager),
        lexer_(lexer),
        modified_file_ids_(modified_file_ids)
    {}

    bool VisitFunctionDecl(FunctionDecl *f)
    {
        currentFunctionName = f->getNameInfo().getName().getAsString();

        // get start and end location of function
        SourceLocation startLocation = f->getBeginLoc();
        SourceLocation endLocation = f->getEndLoc();

        string info = startLocation.printToString(m_sourceManager);

        // get presumed line number of start and end location
        unsigned int startLineNum = m_sourceManager.getPresumedLineNumber(startLocation);
        unsigned int endLineNum = m_sourceManager.getPresumedLineNumber(endLocation);

        // if function is a method, get class name
        int class_flag = 0;
        currentFunctionClassName = "None";
        if (CXXMethodDecl *methodDecl = dyn_cast<CXXMethodDecl>(f)) {
            class_flag = 1;
            currentFunctionClassName = methodDecl->getParent()->getNameAsString();
        }

        // get originated file information of this function
        const FileEntry *fileEntry = m_sourceManager.getFileEntryForID(m_sourceManager.getFileID(startLocation));
        std::string fileName = (fileEntry ? string(fileEntry->getName()) : "UnknownFile");

        // Get function parameters
        string parametersStr;
        for (const ParmVarDecl *param : f->parameters()) {
            if (!parametersStr.empty()) {
                parametersStr += ", ";
            }
            parametersStr += param->getType().getAsString() + " " + param->getNameAsString();
        }
        parametersStr = "(" + parametersStr + ")";
        currentFunctionName = currentFunctionName + parametersStr;

        llvm::outs() << currentFunctionClassName << "##"
                        << currentFunctionName << "##"
                        << startLineNum << "##"
                        << endLineNum << "##"
                        << info << "##"
                        << fileName << "\n";

        return true;
    }

private:
    Rewriter &TheRewriter;
    const LangOptions &LangOpts;
    SourceManager &m_sourceManager;
    Lexer &lexer_;
    set<FileID> &modified_file_ids_;
    std::string currentFunctionName;
    std::string currentFunctionClassName;
};

class MyASTConsumer : public ASTConsumer
{
public:
    MyASTConsumer(
        Rewriter &R,
        const LangOptions &langOptions,
        SourceManager &sourceManager,
        Lexer &lexeer,
        set<FileID> &modified_file_ids
    ) : Visitor(
        R, langOptions, sourceManager,
        lexeer, modified_file_ids
    ) //initialize MyASTVisitor
    {}

    virtual bool HandleTopLevelDecl(DeclGroupRef DR) {
        for (DeclGroupRef::iterator b = DR.begin(), e = DR.end(); b != e; ++b) {
            // Travel each function declaration using MyASTVisitor
            Visitor.TraverseDecl(*b);
        }
        return true;
    }

private:
    MyASTVisitor Visitor;
};

class InsertPublicAction : public ASTFrontendAction {
    public:
        InsertPublicAction() {};
    
    protected:
        unique_ptr<ASTConsumer> CreateASTConsumer(
            CompilerInstance &CI, llvm::StringRef InFile
        ) {
            SourceManager &source_manager = CI.getSourceManager();
            LangOptions &lang_opts = CI.getLangOpts();

            rewriter_.setSourceMgr(source_manager, lang_opts);

            auto file_entry_opt = CI.getFileManager().getFile(InFile);

            if (error_code ec = file_entry_opt.getError()) {
                return nullptr;
            }

            const FileEntry *FileIn = file_entry_opt.get();

            FileID input_fileid =
                source_manager.getOrCreateFileID(FileIn, SrcMgr::C_User);
            
            auto membuf_ptr = llvm::MemoryBuffer::getMemBuffer(InFile);
            llvm::MemoryBufferRef membuf_ref = membuf_ptr->getMemBufferRef();
            Lexer lexer(input_fileid, membuf_ref, source_manager, lang_opts);

            return make_unique<MyASTConsumer>(
                rewriter_, lang_opts, source_manager,
                lexer, modified_file_ids_
            );
        };

        void ExecuteAction() {
            ASTFrontendAction::ExecuteAction();
        };
    
    private:
    Rewriter rewriter_;
    set<FileID> modified_file_ids_{};
};


int main(int argc, char *argv[])
{
    if (argc != 2) {
        llvm::errs() << "Usage: kcov-branch-identify <filename>\n";
        return 1;
    }

    std::ifstream input_file(argv[1]);
    stringstream buffer;
    buffer << input_file.rdbuf();
    input_file.close();

    vector<string> args;
    // args.push_back(argv[2]);

    tooling::runToolOnCodeWithArgs(
        make_unique<InsertPublicAction>(),
        buffer.str(), args, argv[1]
    );

    return 0;
}
