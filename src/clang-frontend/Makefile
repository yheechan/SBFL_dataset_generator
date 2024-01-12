# Target file name which uses clang library
# $(TARGET_CXX) will be compiled and $(TARGET) will be executable file name
TARGET := extractor
TARGET_CXX := $(TARGET).cpp

all: $(TARGET)
.PHONY: all

ifeq (, $(shell which llvm-config))
$(error "No llvm-config in $$PATH")
endif

LLVM_VER  = $(shell llvm-config --version 2>/dev/null | sed 's/git//' | sed 's/svn//' )
LLVM_MAJOR = $(shell llvm-config --version 2>/dev/null | sed 's/\..*//' )
$(info Using LLVM version : $(LLVM_VER))

CXX := clang++
CXXFLAGS := -fno-rtti -O0 -g 

LLVM_CXXFLAGS := `llvm-config --cxxflags`
LLVM_LDFLAGS := `llvm-config --ldflags --libs --system-libs`

CLANG_LIBS := \
	-Wl,--start-group \
	-lclangAST \
	-lclangASTMatchers \
	-lclangAnalysis \
	-lclangBasic \
	-lclangDriver \
	-lclangEdit \
	-lclangFrontend \
	-lclangFrontendTool \
	-lclangLex \
	-lclangParse \
	-lclangSema \
	-lclangEdit \
	-lclangRewrite \
	-lclangRewriteFrontend \
	-lclangStaticAnalyzerFrontend \
	-lclangStaticAnalyzerCheckers \
	-lclangStaticAnalyzerCore \
	-lclangSerialization \
	-lclangToolingCore \
	-lclangTooling \
	-lclangFormat \
	-Wl,--end-group

$(TARGET): $(TARGET_CXX)
	$(CXX) $(CXXFLAGS) $(LLVM_CXXFLAGS) $^ \
	$(CLANG_LIBS) $(LLVM_LDFLAGS) -o $@

clean:
	rm -rf *.o $(TARGET)
